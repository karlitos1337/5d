"""
Caching utilities for 5D Dashboard

Provides:
- Cache configuration constants
- Preload critical data function
- Cache invalidation helpers
- Memory usage monitoring
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any


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
    STATIC = 3600      # 1 hour - Static reference data
    DYNAMIC = 1800     # 30 minutes - API data, scraped content
    BASELINE = 3600    # 1 hour - Map baseline (rarely changes)
    REALTIME = 300     # 5 minutes - Frequent updates


# ============================================================================
# Preload Critical Data
# ============================================================================

@st.cache_data(ttl=CacheTTL.STATIC)
def preload_solutions_data() -> Dict[str, Any]:
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
def preload_research_data() -> Dict[str, Any]:
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
def preload_github_data() -> Dict[str, Any]:
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
def preload_map_baseline() -> Dict[str, Any]:
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
        st.warning(f"⚠️ Selective cache invalidation not supported. Use TTL or restart app.")
    else:
        st.cache_data.clear()
        st.success("✅ All caches cleared")


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
# Memory Monitoring
# ============================================================================

def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics (placeholder for future implementation).

    Returns:
        dict: Cache stats (hit rate, memory usage, etc.)
    """
    # Streamlit doesn't expose cache stats directly
    # This is a placeholder for future custom caching (Redis)
    return {
        "cache_backend": "streamlit",
        "ttl_config": {
            "static": CacheTTL.STATIC,
            "dynamic": CacheTTL.DYNAMIC,
            "baseline": CacheTTL.BASELINE,
            "realtime": CacheTTL.REALTIME,
        },
        "note": "For detailed stats, consider Redis backend"
    }


def display_cache_info():
    """
    Display cache configuration info in Streamlit sidebar.

    Example:
        with st.sidebar:
            display_cache_info()
    """
    with st.expander("⚙️ Cache Configuration", expanded=False):
        st.markdown("""
        **Cache TTL Settings:**
        - 🟢 **Static Data**: 1 hour (BibTeX, schools)
        - 🟡 **Dynamic Data**: 30 min (Research, GitHub)
        - 🔵 **Baseline**: 1 hour (Map data)
        - 🔴 **Realtime**: 5 min (Live metrics)
        
        Data is automatically refreshed after TTL expires.
        """)

        stats = get_cache_stats()
        st.json(stats)


# ============================================================================
# Redis Integration (Future)
# ============================================================================

# TODO: Redis backend for persistent caching across sessions
# - Connection pool configuration
# - Serialization (JSON/Pickle)
# - Key namespacing (5d:solutions:*, 5d:research:*, etc.)
# - TTL synchronization with CacheTTL class
# - Cache warming on deployment
#
# Example implementation:
#
# import redis
#
# class RedisCache:
#     def __init__(self):
#         self.client = redis.Redis(
#             host='localhost',
#             port=6379,
#             db=0,
#             decode_responses=True
#         )
#
#     def get(self, key: str) -> Any:
#         value = self.client.get(f"5d:{key}")
#         return json.loads(value) if value else None
#
#     def set(self, key: str, value: Any, ttl: int = CacheTTL.STATIC):
#         self.client.setex(
#             f"5d:{key}",
#             ttl,
#             json.dumps(value)
#         )
