"""
Caching utilities for the 5D application.
Handles data persistence, expiration, and efficient retrieval.
"""

import json
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any

import redis
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheTTL(Enum):
    """Time-to-live constants in seconds."""

    STATIC = 86400  # 24 hours
    DYNAMIC = 3600  # 1 hour
    REALTIME = 60  # 1 minute
    BASELINE = 86400 * 7  # 1 week


# --- Redis Connection (Optional) ---
def get_redis_client():
    """
    Get Redis client if available.

    Returns:
        redis.Redis or None: Redis client instance
    """
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return None

    try:
        return redis.from_url(redis_url)
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {e}")
        return None


# --- Preloading Functions ---
@st.cache_data(ttl=CacheTTL.STATIC.value)
def preload_solutions_data() -> dict[str, Any]:
    """
    Preload 5d_solutions.json on app startup.

    Returns:
        dict: Parsed solutions data
    """
    try:
        path = Path("5d_solutions.json")
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading solutions data: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.DYNAMIC.value)
def preload_research_data() -> dict[str, Any]:
    """
    Preload 5d_research_data.json on app startup.

    Returns:
        dict: Parsed research data
    """
    try:
        path = Path("5d_research_data.json")
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading research data: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.DYNAMIC.value)
def preload_github_data() -> dict[str, Any]:
    """
    Preload 5d_github_data.json on app startup.

    Returns:
        dict: Parsed GitHub data
    """
    try:
        path = Path("5d_github_data.json")
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading GitHub data: {e}")
        return {}


@st.cache_data(ttl=CacheTTL.BASELINE.value)
def preload_map_baseline() -> dict[str, Any]:
    """
    Preload web/5d-map/data/baseline.json for World Map.

    Returns:
        dict: Parsed baseline data
    """
    try:
        path = Path("web/5d-map/data/baseline.json")
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading baseline map data: {e}")
        return {}


def preload_all_critical_data():
    """Execute all preload functions to warm up the cache."""
    with st.spinner("Lade Daten in Cache..."):
        preload_solutions_data()
        preload_research_data()
        preload_github_data()
        preload_map_baseline()


# --- Cache Management ---
def clear_all_caches():
    """Clear all Streamlit caches."""
    st.cache_data.clear()
    st.cache_resource.clear()
    logger.info("Cache cleared.")


def invalidate_specific_cache(cache_name):
    """
    Invalidate specific cache entries.

    Args:
        cache_name: Name of the cache to clear
    """
    # Streamlit doesn't support selective invalidation in @st.cache_data
    # Use st.cache_data.clear() for all or rely on TTL
    if cache_name == "all":
        st.cache_data.clear()
    else:
        st.warning("⚠️ Selective cache invalidation not supported. Use TTL or restart app.")


def get_cache_size():
    """
    Estimate cache size (memory usage).

    Returns:
        str: Human-readable size
    """
    # Placeholder: Real memory estimation is complex in Python
    return "Unknown"


# --- Persistent Storage (JSON/Redis) ---
class PersistentStore:
    """Handles data persistence across sessions."""

    def __init__(self, use_redis=False):
        self.use_redis = use_redis
        self.redis_client = get_redis_client() if use_redis else None
        self.local_dir = Path("storage/cache")
        self.local_dir.mkdir(parents=True, exist_ok=True)

    def set(self, key, value, ttl=None):
        """
        Save data to storage.

        Args:
            key: Unique key
            value: Data to save (must be JSON serializable)
            ttl: Time to live in seconds (Redis only)
        """
        try:
            serialized = json.dumps(value)
            if self.use_redis and self.redis_client:
                self.redis_client.set(key, serialized, ex=ttl)
            else:
                # Local JSON fallback
                file_path = self.local_dir / f"{key}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(serialized)
        except Exception as e:
            logger.error(f"Failed to save {key}: {e}")

    def get(self, key):
        """
        Retrieve data from storage.

        Args:
            key: Unique key

        Returns:
            Any: Data or None if not found
        """
        try:
            if self.use_redis and self.redis_client:
                data = self.redis_client.get(key)
                return json.loads(data) if data else None
            else:
                # Local JSON fallback
                file_path = self.local_dir / f"{key}.json"
                if file_path.exists():
                    with open(file_path, encoding="utf-8") as f:
                        return json.load(f)
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve {key}: {e}")
            return None

    def delete(self, key):
        """Delete data from storage."""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.delete(key)
            else:
                file_path = self.local_dir / f"{key}.json"
                if file_path.exists():
                    file_path.unlink()
        except Exception as e:
            logger.error(f"Failed to delete {key}: {e}")


# --- Session State Helpers ---
def init_session_state(key, default_value):
    """
    Initialize a session state variable if it doesn't exist.

    Args:
        key: Variable name
        default_value: Initial value
    """
    if key not in st.session_state:
        st.session_state[key] = default_value


def get_state(key):
    """Get session state value safely."""
    return st.session_state.get(key)


def set_state(key, value):
    """Set session state value."""
    st.session_state[key] = value


# --- Advanced Caching Strategies ---
def memoize_with_fallback(func, fallback_value=None):
    """
    Decorator to wrap a function with try-except and caching.

    Args:
        func: Function to wrap
        fallback_value: Value to return on failure

    Returns:
        Wrapped function
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Function {func.__name__} failed: {e}")
            return fallback_value

    return wrapper


# --- Visualization Cache ---
@st.cache_data(ttl=CacheTTL.STATIC.value)
def cache_chart(fig):
    """
    Cache a Plotly figure to avoid re-rendering.
    Note: Plotly objects can be large, use sparingly.

    Args:
        fig: Plotly figure object

    Returns:
        fig: The same figure
    """
    return fig


# --- Data Transformation Cache ---
@st.cache_data
def robust_dataframe_transformation(df, transform_func):
    """
    Apply a transformation to a DataFrame and cache the result.

    Args:
        df: Input DataFrame
        transform_func: Function to apply

    Returns:
        Transformed DataFrame
    """
    return transform_func(df)


# --- Dashboard Status ---
def display_cache_info():
    """Display cache status in the sidebar."""
    with st.sidebar.expander("🛠️ System Status"):
        st.write(f"**Python:** {sys.version.split()[0]}")
        st.write(f"**Streamlit:** {st.__version__}")

        if st.button("🗑️ Cache leeren"):
            clear_all_caches()
            st.rerun()

        # Check Redis
        redis_client = get_redis_client()
        if redis_client:
            try:
                redis_client.ping()
                st.success("Redis: Verbunden ✅")
            except Exception:
                st.error("Redis: Fehler ❌")
        else:
            st.info("Redis: Nicht konfiguriert ⚪")


import sys  # noqa: E402


def get_cache_stats() -> dict[str, Any]:
    """
    Get cache statistics.

    Returns:
        dict: Stats like size, hits, misses (mocked for now)
    """
    return {
        "memory_usage": get_cache_size(),
        "entries": "N/A",  # Streamlit doesn't expose this easily
        "redis_connected": bool(get_redis_client()),
    }
