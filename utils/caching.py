"""
Caching utilities for 5D-Intelligence App.
Handles data persistence, preloading, and cache invalidation strategies.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any

import redis
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Redis Configuration (Optional - Falls back to local file cache)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
USE_REDIS = os.getenv("USE_REDIS", "false").lower() == "true"

try:
    if USE_REDIS:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        logger.info("✅ Redis Cache Enabled")
    else:
        redis_client = None
        logger.info("ℹ️ Redis Cache Disabled (Using Local File Cache)")
except Exception as e:
    logger.error(f"❌ Redis Connection Failed: {e}")
    redis_client = None


class CacheTTL:
    """Time-To-Live constants for different data types."""
    STATIC = 3600 * 24 * 7  # 1 Week (e.g., Solutions, Theory)
    BASELINE = 3600 * 24    # 1 Day (e.g., World Map Base Data)
    DYNAMIC = 3600          # 1 Hour (e.g., Live Research, Github Stats)
    REALTIME = 60           # 1 Minute (e.g., User Session State)


# ============================================================================
# 1. CORE DATA PRELOADING (Static/Baseline)
# ============================================================================

@st.cache_data(ttl=CacheTTL.STATIC)
def preload_solutions_data() -> dict[str, Any]:
    """
    Preload 5d_solutions.json on app startup.
    This data is static and rarely changes.
    """
    filepath = Path("5d_solutions.json")
    if not filepath.exists():
        logger.warning(f"⚠️ {filepath} not found.")
        return {}

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"✅ Loaded {len(data)} solutions.")
        return data
    except Exception as e:
        logger.error(f"❌ Error loading solutions: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_research_data() -> dict[str, Any]:
    """
    Preload 5d_research_data.json on app startup.
    This data is updated by the scraper.
    """
    filepath = Path("5d_research_data.json")
    if not filepath.exists():
        logger.warning(f"⚠️ {filepath} not found.")
        return {}

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info("✅ Loaded research data.")
        return data
    except Exception as e:
        logger.error(f"❌ Error loading research data: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_github_data() -> dict[str, Any]:
    """
    Preload 5d_github_data.json on app startup.
    This data is updated by the GitHub API scraper.
    """
    filepath = Path("5d_github_data.json")
    if not filepath.exists():
        logger.warning(f"⚠️ {filepath} not found.")
        return {}

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info("✅ Loaded GitHub data.")
        return data
    except Exception as e:
        logger.error(f"❌ Error loading GitHub data: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.BASELINE)
def preload_map_baseline() -> dict[str, Any]:
    """
    Preload web/5d-map/data/baseline.json for World Map.
    """
    filepath = Path("web/5d-map/data/baseline.json")
    # Check alternate location if running from root
    if not filepath.exists():
        filepath = Path("data/baseline.json")

    if not filepath.exists():
        logger.warning(f"⚠️ Map baseline data not found at {filepath}")
        return {}

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info("✅ Loaded Map Baseline data.")
        return data
    except Exception as e:
        logger.error(f"❌ Error loading Map Baseline: {e}")
        return {}


# ============================================================================
# 2. CACHE MANAGEMENT
# ============================================================================

def get_cached_value(key: str) -> Any | None:
    """
    Retrieve value from cache (Redis or Local File).
    """
    # 1. Try Redis
    if redis_client:
        try:
            val = redis_client.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.warning(f"Redis get failed: {e}")

    # 2. Try File Cache
    file_path = CACHE_DIR / f"{key}.json"
    if file_path.exists():
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"File cache read failed: {e}")

    return None


def set_cached_value(key: str, value: Any, ttl: int = CacheTTL.DYNAMIC):
    """
    Set value in cache (Redis and Local File).
    """
    json_val = json.dumps(value)

    # 1. Redis
    if redis_client:
        try:
            redis_client.setex(key, ttl, json_val)
        except Exception as e:
            logger.warning(f"Redis set failed: {e}")

    # 2. File Cache (No TTL support natively, just persistent)
    try:
        file_path = CACHE_DIR / f"{key}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_val)
    except Exception as e:
        logger.warning(f"File cache write failed: {e}")


def invalidate_cache(key: str = None):
    """
    Invalidate cache.
    If key is None, clears ALL cache (Streamlit + Custom).
    """
    if key:
        # Streamlit doesn't support selective invalidation in @st.cache_data
        # Use st.cache_data.clear() for all or rely on TTL
        st.warning("⚠️ Selective cache invalidation not supported. Use TTL or restart app.")
    else:
        st.cache_data.clear()

        # Clear custom file cache
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()

        # Clear Redis
        if redis_client:
            redis_client.flushdb()

        logger.info("🧹 Cache Cleared!")


# ============================================================================
# 3. HELPER: DATA LOADER WITH FALLBACK
# ============================================================================

def load_data_with_fallback(primary_key: str, fallback_function, ttl: int = CacheTTL.DYNAMIC) -> Any:
    """
    Generic loader:
    1. Check Cache
    2. If miss, run fallback_function()
    3. Save to Cache
    4. Return Data
    """
    # 1. Check Cache
    cached = get_cached_value(primary_key)
    if cached:
        logger.info(f"⚡ Cache Hit: {primary_key}")
        return cached

    # 2. Run Fallback (Fetch Data)
    logger.info(f"🔄 Cache Miss: Fetching {primary_key}...")
    try:
        data = fallback_function()
    except Exception as e:
        logger.error(f"❌ Data fetch failed: {e}")
        return None

    # 3. Save to Cache
    if data:
        set_cached_value(primary_key, data, ttl)
        return data

    return None


# ============================================================================
# 4. MONITORING
# ============================================================================

def check_redis_health() -> bool:
    """Check if Redis is responsive."""
    if not redis_client:
        return False
    try:
        return redis_client.ping()
    except Exception:
        return False

# ============================================================================
# 5. INITIALIZATION
# ============================================================================

def init_app_state():
    """
    Initialize Session State with preloaded data.
    Should be called at the start of the main app.
    """
    if "data_loaded" not in st.session_state:
        with st.spinner("🚀 Booting 5D-Intelligence Node..."):
            st.session_state["solutions"] = preload_solutions_data()
            st.session_state["research"] = preload_research_data()
            st.session_state["github"] = preload_github_data()
            st.session_state["map_baseline"] = preload_map_baseline()

            st.session_state["data_loaded"] = True

            # Health Check
            if check_redis_health():
                st.toast("✅ Redis Cache Active", icon="⚡")
            else:
                st.toast("ℹ️ Using Local Cache", icon="📂")

# ============================================================================
# 6. CACHE STATS
# ============================================================================

def get_cache_stats() -> dict[str, Any]:
    """
    Get cache statistics.
    """
    stats = {
        "type": "Redis" if redis_client else "Local File",
        "status": "Healthy" if check_redis_health() or not redis_client else "Error",
        "file_cache_count": len(list(CACHE_DIR.glob("*.json"))),
        "file_cache_size_kb": sum(f.stat().st_size for f in CACHE_DIR.glob("*.json")) / 1024
    }

    if redis_client:
        try:
            info = redis_client.info()
            stats["redis_keys"] = redis_client.dbsize()
            stats["redis_used_memory_human"] = info["used_memory_human"]
        except Exception:
            stats["redis_error"] = "Could not fetch stats"

    return stats
