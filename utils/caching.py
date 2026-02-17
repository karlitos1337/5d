"""
Caching utilities for 5D Dashboard

Provides:
- Cache configuration constants
- Preload critical data function
- Cache invalidation helpers
- Memory usage monitoring
- Redis backend for persistent caching
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

# ============================================================================
# Cache TTL Configuration
# ============================================================================


class CacheTTL:
    """
    Cache Time-To-Live configuration for different data types.

    Values in seconds:
    - STATIC: 3600s (1 hour) - Rarely changes (BibTeX, alternative schools, etc.)
    - DYNAMIC: 1800s (30 minutes) - Updated occasionally (research data, GitHub API)
    - BASELINE: 3600s (1 hour) - World map baseline data (from 5d-map)
    - REALTIME: 300s (5 minutes) - Frequently updated (user inputs, live metrics)
    """

    STATIC = 3600  # 1 hour - Static reference data
    DYNAMIC = 1800  # 30 minutes - API data, scraped content
    BASELINE = 3600  # 1 hour - Map baseline (rarely changes)
    REALTIME = 300  # 5 minutes - Frequent updates


# ============================================================================
# Preload Critical Data
# ============================================================================


@st.cache_data(ttl=CacheTTL.STATIC)
def preload_solutions_data() -> dict[str, Any]:
    """
    Preload 5d_solutions.json on app startup.

    Returns:
        dict: Solutions data or empty dict if not found
    """
    try:
        with open("5d_solutions.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"solutions": [], "metadata": {}}
    except Exception as e:
        st.error(f"❌ Error loading solutions: {e}")
        return {"solutions": [], "metadata": {}}


@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_research_data() -> dict[str, Any]:
    """
    Preload 5d_research_data.json on app startup.

    Returns:
        dict: Research data or empty dict if not found
    """
    try:
        with open("5d_research_data.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        st.error(f"❌ Error loading research data: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_github_data() -> dict[str, Any]:
    """
    Preload 5d_github_data.json on app startup.

    Returns:
        dict: GitHub data or empty dict if not found
    """
    try:
        with open("5d_github_data.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        st.error(f"❌ Error loading GitHub data: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.BASELINE)
def preload_map_baseline() -> dict[str, Any]:
    """
    Preload web/5d-map/data/baseline.json for World Map.

    Returns:
        dict: Baseline map data or empty dict if not found
    """
    try:
        with open("web/5d-map/data/baseline.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        st.error(f"❌ Error loading map baseline: {e}")
        return {}


def preload_all_critical_data():
    """
    Preload all critical data on app startup.

    Call this in main dashboard (5d_dashboard.py) to warm up caches.

    Example:
        from utils.caching import preload_all_critical_data

        def main():
            preload_all_critical_data()
            st.title("5D Dashboard")
            # ... rest of app
    """
    preload_solutions_data()
    preload_research_data()
    preload_github_data()
    preload_map_baseline()


# ============================================================================
# Cache Invalidation
# ============================================================================


def invalidate_cache(cache_key: str = None):
    """
    Invalidate Streamlit cache.

    Args:
        cache_key: Specific cache key to clear (None = clear all)

    Example:
        # Clear all caches
        invalidate_cache()

        # Clear specific function cache
        invalidate_cache("load_research_data")
    """
    if cache_key:
        # Streamlit doesn't support selective invalidation in @st.cache_data
        # Use st.cache_data.clear() for all or rely on TTL
        st.warning(
            "⚠️ Selective cache invalidation not supported. Use TTL or restart app."
        )
    else:
        st.cache_data.clear()
        st.success("✅ All caches cleared")

    # Also invalidate Redis cache if enabled
    if "redis_cache" in globals() and redis_cache._enabled:
        redis_cache.invalidate(cache_key)
        if not cache_key:
            logger.info("Redis cache cleared")


def force_refresh_on_schema_update():
    """
    Force cache refresh when schema is updated.

    Usage: Call this after schema changes in models/schemas.py

    Checks:
    - models/schemas.py modification time
    - Compare with last known cache timestamp
    """
    schema_path = Path("models/schemas.py")

    if not schema_path.exists():
        return

    schema_mtime = schema_path.stat().st_mtime

    # Store in session state
    if "schema_cache_timestamp" not in st.session_state:
        st.session_state.schema_cache_timestamp = schema_mtime
        return

    # Check if schema was modified since last cache
    if schema_mtime > st.session_state.schema_cache_timestamp:
        st.cache_data.clear()
        st.session_state.schema_cache_timestamp = schema_mtime
        st.info("🔄 Schema updated - caches refreshed")


# ============================================================================
# Redis Integration
# ============================================================================


class RedisCache:
    """
    Redis backend for persistent caching across sessions.
    Handles connection pooling, serialization, and namespacing.
    """

    def __init__(
        self,
        host: str = None,
        port: int = None,
        db: int = 0,
        password: str = None,
        socket_connect_timeout: int = 5,
    ):
        """
        Initialize Redis connection with pooling.

        Args:
            host: Redis host (default: env REDIS_HOST or 'localhost')
            port: Redis port (default: env REDIS_PORT or 6379)
            db: Redis DB index (default: env REDIS_DB or 0)
            password: Redis password (default: env REDIS_PASSWORD or None)
        """
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.db = db or int(os.getenv("REDIS_DB", 0))
        self.password = password or os.getenv("REDIS_PASSWORD", None)

        self.pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True,
            socket_connect_timeout=socket_connect_timeout,
        )
        self.client = redis.Redis(connection_pool=self.pool)
        self.namespace = "5d"
        self._enabled = True

        # Test connection
        try:
            self.client.ping()
            logger.info("✅ Redis connected successfully")
        except redis.ConnectionError:
            self._enabled = False
            logger.warning("⚠️ Redis connection failed. Caching disabled.")

    def _get_key(self, key: str) -> str:
        """Format key with namespace."""
        return f"{self.namespace}:{key}"

    def get(self, key: str) -> Any:
        """
        Retrieve value from cache.

        Args:
            key: Cache key (without namespace)

        Returns:
            Deserialized value or None if missing/error
        """
        if not self._enabled:
            return None

        try:
            value = self.client.get(self._get_key(key))
            return json.loads(value) if value else None
        except (redis.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Redis get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = CacheTTL.STATIC) -> bool:
        """
        Set value in cache with TTL.

        Args:
            key: Cache key (without namespace)
            value: Data to cache (must be JSON serializable)
            ttl: Time to live in seconds

        Returns:
            bool: True if successful
        """
        if not self._enabled:
            return False

        try:
            serialized = json.dumps(value)
            return self.client.setex(self._get_key(key), ttl, serialized)
        except (redis.RedisError, TypeError) as e:
            logger.error(f"Redis set error: {e}")
            return False

    def invalidate(self, key: str = None):
        """
        Invalidate cache keys.

        Args:
            key: Specific key to delete. If None, clears entire namespace.
        """
        if not self._enabled:
            return

        try:
            if key:
                self.client.delete(self._get_key(key))
            else:
                # Pattern match for namespace
                keys = self.client.keys(f"{self.namespace}:*")
                if keys:
                    self.client.delete(*keys)
        except redis.RedisError as e:
            logger.error(f"Redis invalidate error: {e}")

    def warm_up(self):
        """
        Warm up cache with critical data.
        """
        if not self._enabled:
            return

        logger.info("Starting Redis cache warm-up...")

        # Load data using existing preload functions
        solutions = preload_solutions_data()
        if solutions:
            self.set("solutions", solutions, CacheTTL.STATIC)

        research = preload_research_data()
        if research:
            self.set("research", research, CacheTTL.DYNAMIC)

        github = preload_github_data()
        if github:
            self.set("github", github, CacheTTL.DYNAMIC)

        map_data = preload_map_baseline()
        if map_data:
            self.set("map_baseline", map_data, CacheTTL.BASELINE)

        logger.info("Redis cache warm-up complete.")


# Global instance
redis_cache = RedisCache()


# ============================================================================
# Memory Monitoring
# ============================================================================


def get_cache_stats() -> dict[str, Any]:
    """
    Get cache statistics.

    Returns:
        dict: Cache stats (hit rate, memory usage, etc.)
    """
    stats = {
        "cache_backend": "streamlit",
        "ttl_config": {
            "static": CacheTTL.STATIC,
            "dynamic": CacheTTL.DYNAMIC,
            "baseline": CacheTTL.BASELINE,
            "realtime": CacheTTL.REALTIME,
        },
    }

    if redis_cache._enabled:
        try:
            info = redis_cache.client.info()
            # Extract some useful info
            redis_stats = {
                "connected": True,
                "used_memory_human": info.get("used_memory_human"),
                "total_connections_received": info.get("total_connections_received"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keys": info.get("db0", {}).get("keys", 0) if "db0" in info else 0,
            }
            stats["redis"] = redis_stats
            stats["cache_backend"] = "streamlit + redis"
        except Exception as e:
            stats["redis"] = {"connected": False, "error": str(e)}

    return stats


def display_cache_info():
    """
    Display cache configuration info in Streamlit sidebar.

    Example:
        with st.sidebar:
            display_cache_info()
    """
    with st.expander("⚙️ Cache Configuration", expanded=False):
        st.markdown(
            """
        **Cache TTL Settings:**
        - 🟢 **Static Data**: 1 hour (BibTeX, schools)
        - 🟡 **Dynamic Data**: 30 min (Research, GitHub)
        - 🔵 **Baseline**: 1 hour (Map data)
        - 🔴 **Realtime**: 5 min (Live metrics)
        
        Data is automatically refreshed after TTL expires.
        """
        )

        stats = get_cache_stats()
        st.json(stats)
