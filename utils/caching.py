# Caching Utilities for 5D Framework
# Implements multi-level caching strategies (RAM, LocalStorage, Redis) to optimize performance.

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

# --- Redis Configuration ---
# Fallback to None if not configured, enabling graceful degradation to local cache
REDIS_URL = os.getenv("REDIS_URL")
redis_client = None

if REDIS_URL:
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        # Test connection
        redis_client.ping()
        logger.info("✅ Connected to Redis cache.")
    except redis.ConnectionError:
        logger.warning("⚠️ Could not connect to Redis. Falling back to local/memory cache.")
        redis_client = None
else:
    logger.info("ℹ️ No REDIS_URL found. Using local/memory cache.")

# --- Constants ---
CACHE_PREFIX = "5d_cache:"

class CacheTTL:
    """Standard Time-To-Live values in seconds."""
    SHORT = 60 * 5          # 5 minutes
    MEDIUM = 60 * 60        # 1 hour
    LONG = 60 * 60 * 24     # 24 hours
    STATIC = 60 * 60 * 24 * 30 # 30 days (effectively static)
    DYNAMIC = 60 * 15       # 15 minutes (for frequently updating data)
    BASELINE = 60 * 60 * 24 * 7 # 1 week (for baseline data)

# --- Preloader Functions (Streamlit) ---
# These functions use @st.cache_data for session-level caching in Streamlit

@st.cache_data(ttl=CacheTTL.STATIC)
def preload_solutions_data() -> dict[str, Any]:
    """
    Preload 5d_solutions.json on app startup.
    Returns:
        dict: The loaded solutions data.
    """
    filepath = Path("5d_solutions.json")
    if not filepath.exists():
        logger.warning(f"File not found: {filepath}")
        return {}

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} solutions from {filepath}")
        return data
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {filepath}")
        return {}

@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_research_data() -> dict[str, Any]:
    """
    Preload 5d_research_data.json on app startup.
    Returns:
        dict: The loaded research data.
    """
    filepath = Path("5d_research_data.json")
    if not filepath.exists():
        logger.warning(f"File not found: {filepath}")
        return {}

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded research data from {filepath}")
        return data
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {filepath}")
        return {}

@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_github_data() -> dict[str, Any]:
    """
    Preload 5d_github_data.json on app startup.
    Returns:
        dict: The loaded GitHub data.
    """
    filepath = Path("5d_github_data.json")
    if not filepath.exists():
        logger.warning(f"File not found: {filepath}")
        return {}

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded GitHub data from {filepath}")
        return data
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {filepath}")
        return {}

@st.cache_data(ttl=CacheTTL.BASELINE)
def preload_map_baseline() -> dict[str, Any]:
    """
    Preload web/5d-map/data/baseline.json for World Map.
    Returns:
        dict: The loaded baseline data.
    """
    filepath = Path("web/5d-map/data/baseline.json")
    if not filepath.exists():
        logger.warning(f"File not found: {filepath}")
        return {}

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded baseline data from {filepath}")
        return data
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {filepath}")
        return {}

# --- Cache Management ---

def get_from_cache(key: str) -> Any | None:
    """
    Retrieve value from cache (Redis if available, else Streamlit session state fallback).

    Args:
        key (str): The cache key.

    Returns:
        Any | None: The cached value or None if not found.
    """
    full_key = f"{CACHE_PREFIX}{key}"

    # 1. Try Redis
    if redis_client:
        try:
            val = redis_client.get(full_key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.error(f"Redis read error: {e}")

    # 2. Fallback: Streamlit Session State (Simulated Local Memory)
    # Note: In a real multi-user app, this only persists per session.
    if "local_cache" not in st.session_state:
        st.session_state.local_cache = {}

    return st.session_state.local_cache.get(full_key)

def set_to_cache(key: str, value: Any, ttl: int = CacheTTL.MEDIUM):
    """
    Set value in cache (Redis if available, else Streamlit session state).

    Args:
        key (str): The cache key.
        value (Any): The value to cache (must be JSON serializable).
        ttl (int): Time to live in seconds.
    """
    full_key = f"{CACHE_PREFIX}{key}"

    # 1. Try Redis
    if redis_client:
        try:
            serialized = json.dumps(value)
            redis_client.setex(full_key, ttl, serialized)
            return
        except Exception as e:
            logger.error(f"Redis write error: {e}")

    # 2. Fallback: Streamlit Session State
    if "local_cache" not in st.session_state:
        st.session_state.local_cache = {}

    st.session_state.local_cache[full_key] = value

def invalidate_cache(key_pattern: str = "*"):
    """
    Invalidate cache keys matching a pattern.

    Args:
        key_pattern (str): Redis-style glob pattern (default: "*").
    """
    # 1. Redis
    if redis_client:
        try:
            full_pattern = f"{CACHE_PREFIX}{key_pattern}"
            keys = redis_client.keys(full_pattern)
            if keys:
                redis_client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} Redis keys matching '{full_pattern}'")
        except Exception as e:
            logger.error(f"Redis delete error: {e}")

    # 2. Streamlit Session State
    if "local_cache" in st.session_state:
        # Simple glob-like matching not fully implemented for dict, just clearing all for safety if pattern is broad
        if key_pattern == "*":
            st.session_state.local_cache = {}
            logger.info("Cleared local session cache.")
        else:
            # Basic suffix matching
            keys_to_del = [k for k in st.session_state.local_cache.keys() if key_pattern.strip("*") in k]
            for k in keys_to_del:
                del st.session_state.local_cache[k]

def clear_app_cache():
    """
    Clears all application cache (both data cache and resource cache).
    Useful for 'Reset' buttons.
    """
    # Clear Streamlit cache
    if hasattr(st, "cache_data"):
        # Streamlit doesn't support selective invalidation in @st.cache_data
        # Use st.cache_data.clear() for all or rely on TTL
        st.warning("⚠️ Selective cache invalidation not supported. Use TTL or restart app.")
    else:
        st.cache_data.clear()

    # Clear Custom Redis/Local Cache
    invalidate_cache("*")

    logger.info("🧹 Application cache cleared.")

# --- Advanced Caching Decorator (Optional) ---
# Can be used to wrap expensive functions independent of Streamlit

def cached(ttl: int = CacheTTL.MEDIUM):
    """
    Decorator to cache function results in Redis/Local.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create a key based on function name and arguments
            # Note: This is a simplistic key generation.
            key_part = f"{func.__name__}:{args}:{kwargs}"
            # Hash it to be safe
            import hashlib
            key_hash = hashlib.md5(key_part.encode()).hexdigest()

            cached_val = get_from_cache(key_hash)
            if cached_val is not None:
                return cached_val

            result = func(*args, **kwargs)
            set_to_cache(key_hash, result, ttl)
            return result
        return wrapper
    return decorator

# --- Knowledge Graph Caching ---

@st.cache_resource
def get_shared_knowledge_graph():
    """
    Returns a shared instance of the Knowledge Graph (if applicable).
    Uses st.cache_resource for objects that shouldn't be serialized/copied (like DB connections or large graphs).
    """
    # Placeholder for actual graph initialization
    # form knowledge_graph.core import KnowledgeGraph
    # return KnowledgeGraph()
    return None

# --- Cache Inspection (Admin) ---

def get_cache_stats() -> dict[str, Any]:
    """
    Get cache statistics.
    Returns:
        dict: Stats like hit rate, memory usage (if available).
    """
    stats = {
        "backend": "Redis" if redis_client else "Local Memory",
        "redis_connected": bool(redis_client),
    }

    if redis_client:
        try:
            info = redis_client.info()
            stats.update({
                "used_memory_human": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "keys_count": len(redis_client.keys(f"{CACHE_PREFIX}*"))
            })
        except Exception:
            stats["error"] = "Could not fetch Redis stats"

    if "local_cache" in st.session_state:
        stats["local_keys_count"] = len(st.session_state.local_cache)
        
    return stats
