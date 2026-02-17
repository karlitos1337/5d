"""
Caching utilities for the application.
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
# Redis Configuration
# ============================================================================

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    redis_client.ping() # Check connection
    logger.info("Connected to Redis.")
except redis.ConnectionError:
    logger.warning("Could not connect to Redis. Caching will be disabled or fall back to memory.")
    redis_client = None

# ============================================================================
# Caching Decorators & Functions
# ============================================================================

class CacheTTL:
    """Standard TTLs in seconds."""
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    STATIC = None # Never expire (until restart/cleared)
    DYNAMIC = 300 # 5 minutes for frequently changing data
    BASELINE = 3600 # 1 hour for baseline data

@st.cache_data(ttl=CacheTTL.STATIC)
def preload_solutions_data() -> dict[str, Any]:
    """
    Preload 5d_solutions.json on app startup.
    """
    try:
        file_path = Path("5d_solutions.json")
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            logger.info("Preloaded 5d_solutions.json")
            return data
        else:
            logger.warning("5d_solutions.json not found.")
            return {}
    except Exception as e:
        logger.error(f"Error loading 5d_solutions.json: {e}")
        return {}

@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_research_data() -> dict[str, Any]:
    """
    Preload 5d_research_data.json on app startup.
    """
    try:
        file_path = Path("5d_research_data.json")
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            logger.info("Preloaded 5d_research_data.json")
            return data
        else:
            logger.warning("5d_research_data.json not found.")
            return {}
    except Exception as e:
        logger.error(f"Error loading 5d_research_data.json: {e}")
        return {}

@st.cache_data(ttl=CacheTTL.DYNAMIC)
def preload_github_data() -> dict[str, Any]:
    """
    Preload 5d_github_data.json on app startup.
    """
    try:
        file_path = Path("5d_github_data.json")
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            logger.info("Preloaded 5d_github_data.json")
            return data
        else:
            logger.warning("5d_github_data.json not found.")
            return {}
    except Exception as e:
        logger.error(f"Error loading 5d_github_data.json: {e}")
        return {}

@st.cache_data(ttl=CacheTTL.BASELINE)
def preload_map_baseline() -> dict[str, Any]:
    """
    Preload web/5d-map/data/baseline.json for World Map.
    """
    try:
        file_path = Path("web/5d-map/data/baseline.json")
        if file_path.exists():
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            logger.info("Preloaded web/5d-map/data/baseline.json")
            return data
        else:
            logger.warning("web/5d-map/data/baseline.json not found.")
            return {}
    except Exception as e:
        logger.error(f"Error loading baseline.json: {e}")
        return {}

def get_cached_data(key: str, ttl: int = CacheTTL.HOUR) -> Any:
    """
    Retrieve data from Redis cache if available, otherwise return None.
    Use this for data that is expensive to compute/fetch but not suitable for st.cache_data
    (e.g., shared across sessions/users if using external Redis).
    """
    if redis_client:
        try:
            data = redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"Redis get error for {key}: {e}")
    return None

def set_cached_data(key: str, data: Any, ttl: int = CacheTTL.HOUR):
    """
    Set data in Redis cache.
    """
    if redis_client:
        try:
            redis_client.setex(key, ttl, json.dumps(data))
        except Exception as e:
            logger.error(f"Redis set error for {key}: {e}")

def clear_app_cache(selective: bool = False):
    """
    Clear Streamlit cache.
    Args:
        selective (bool): If True, try to clear only specific entries (not fully supported by st.cache_data directly).
                          Currently clears all data to be safe.
    """
    if selective:
        # Streamlit doesn't support selective invalidation in @st.cache_data
        # Use st.cache_data.clear() for all or rely on TTL
        st.warning("⚠️ Selective cache invalidation not supported. Use TTL or restart app.")
    else:
        st.cache_data.clear()
        st.cache_resource.clear()
        if redis_client:
            try:
                redis_client.flushdb()
                logger.info("Redis cache flushed.")
            except Exception as e:
                logger.error(f"Error flushing Redis: {e}")
        logger.info("Streamlit cache cleared.")

# ============================================================================
# Cache Statistics (Optional)
# ============================================================================

def get_cache_stats() -> dict[str, Any]:
    """
    Get cache statistics.
    """
    stats = {
        "streamlit_cache_data_info": "N/A (Streamlit internal)",
        "redis_connected": redis_client is not None
    }
    if redis_client:
        try:
            info = redis_client.info()
            stats["redis_used_memory"] = info.get("used_memory_human")
            stats["redis_connected_clients"] = info.get("connected_clients")
            stats["redis_keys"] = redis_client.dbsize()
        except Exception as e:
            stats["redis_error"] = str(e)

    return stats
