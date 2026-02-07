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


# Cache TTL constants (in seconds)
class CacheTTL:
    STATIC = 3600 * 24  # 24 hours for static files
    DYNAMIC = 300  # 5 minutes for dynamic data
    BASELINE = 3600  # 1 hour for baseline data


# Redis configuration (optional, fallback to in-memory)
REDIS_URL = os.getenv("REDIS_URL")
redis_client = None

if REDIS_URL:
    try:
        redis_client = redis.from_url(REDIS_URL)
        redis_client.ping()
        logger.info("Connected to Redis cache.")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}. Using local cache.")

# ============================================================================
# Core Caching Decorators & Functions
# ============================================================================


@st.cache_data(ttl=CacheTTL.STATIC)
def preload_solutions_data() -> dict[str, Any]:
    """
    Preload 5d_solutions.json on app startup.
    """
    file_path = Path("5d_solutions.json")
    if not file_path.exists():
        logger.warning("5d_solutions.json not found.")
        return {}

    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading 5d_solutions.json: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_research_data() -> dict[str, Any]:
    """
    Preload 5d_research_data.json on app startup.
    """
    file_path = Path("5d_research_data.json")
    if not file_path.exists():
        logger.warning("5d_research_data.json not found.")
        return {}

    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading 5d_research_data.json: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_github_data() -> dict[str, Any]:
    """
    Preload 5d_github_data.json on app startup.
    """
    file_path = Path("5d_github_data.json")
    if not file_path.exists():
        logger.warning("5d_github_data.json not found.")
        return {}

    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading 5d_github_data.json: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.BASELINE)
def preload_map_baseline() -> dict[str, Any]:
    """
    Preload web/5d-map/data/baseline.json for World Map.
    """
    file_path = Path("web/5d-map/data/baseline.json")
    if not file_path.exists():
        logger.warning("baseline.json not found.")
        return {}

    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading baseline.json: {e}")
        return {}


def get_cached_data(key: str) -> Any:
    """
    Retrieve data from cache (Redis or Streamlit session state).
    """
    if redis_client:
        try:
            data = redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception:
            pass

    # Fallback to session state
    return st.session_state.get(f"cache_{key}")


def set_cached_data(key: str, data: Any, ttl: int = 300):
    """
    Set data in cache.
    """
    if redis_client:
        try:
            redis_client.setex(key, ttl, json.dumps(data))
        except Exception:
            pass

    st.session_state[f"cache_{key}"] = data


def clear_cache(key: str = None):
    """
    Clear specific cache key or all cache.
    """
    if key:
        if redis_client:
            redis_client.delete(key)
        if f"cache_{key}" in st.session_state:
            del st.session_state[f"cache_{key}"]

        # Streamlit doesn't support selective invalidation in @st.cache_data
        # Use st.cache_data.clear() for all or rely on TTL
        st.warning("⚠️ Selective cache invalidation not supported. Use TTL or restart app.")
    else:
        st.cache_data.clear()
        if redis_client:
            try:
                redis_client.flushdb()
            except Exception:
                pass
        # Clear session state cache keys
        keys_to_del = [k for k in st.session_state.keys() if k.startswith("cache_")]
        for k in keys_to_del:
            del st.session_state[k]


# ============================================================================
# Advanced Caching Strategies
# ============================================================================


def smart_cache(ttl: int = 300):
    """
    Decorator for smart caching with Redis fallback.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create a unique key based on function name and arguments
            key = f"{func.__name__}_{str(args)}_{str(kwargs)}"

            # Try to get from cache
            cached = get_cached_data(key)
            if cached:
                return cached

            # Execute function
            result = func(*args, **kwargs)

            # Save to cache
            set_cached_data(key, result, ttl)
            return result

        return wrapper

    return decorator


# ============================================================================
# Cache Warming
# ============================================================================


def warm_up_cache():
    """
    Warm up critical caches on startup.
    """
    logger.info("Warming up caches...")
    try:
        preload_solutions_data()
        preload_research_data()
        preload_github_data()
        preload_map_baseline()
        logger.info("Cache warm-up complete.")
    except Exception as e:
        logger.error(f"Cache warm-up failed: {e}")


# ============================================================================
# Cache Statistics
# ============================================================================


def get_cache_stats() -> dict[str, Any]:
    """
    Get cache statistics.
    """
    stats = {"type": "Redis" if redis_client else "Local", "keys": [], "memory_usage": "Unknown"}

    if redis_client:
        try:
            info = redis_client.info()
            stats["keys"] = redis_client.keys("*")
            stats["memory_usage"] = info.get("used_memory_human", "Unknown")
        except Exception:
            pass
    else:
        keys = [k for k in st.session_state.keys() if k.startswith("cache_")]
        stats["keys"] = keys

    return stats
