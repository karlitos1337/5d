#!/usr/bin/env python3
"""
Tests for Token Bucket Rate Limiter
"""

import asyncio
import time
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.rate_limiter import TokenBucketRateLimiter, DomainRateLimiter


class TestTokenBucketRateLimiter:
    """Test token bucket rate limiter"""
    
    @pytest.mark.asyncio
    async def test_basic_rate_limiting(self):
        """Test basic token acquisition"""
        limiter = TokenBucketRateLimiter(rate=2.0)  # 2 tokens per second
        
        # Should allow immediate acquisition
        start = time.monotonic()
        await limiter.acquire(1)
        elapsed = time.monotonic() - start
        
        assert elapsed < 0.1, "First acquisition should be immediate"
    
    @pytest.mark.asyncio
    async def test_burst_capacity(self):
        """Test burst capacity allows multiple rapid requests"""
        limiter = TokenBucketRateLimiter(rate=1.0, max_tokens=5)
        
        # Should allow burst of 5 requests
        start = time.monotonic()
        for _ in range(5):
            await limiter.acquire(1)
        elapsed = time.monotonic() - start
        
        assert elapsed < 0.5, "Burst should be fast"
    
    @pytest.mark.asyncio
    async def test_rate_enforcement(self):
        """Test rate limiting enforcement over time"""
        limiter = TokenBucketRateLimiter(rate=2.0, max_tokens=2)  # 2 tokens/sec
        
        # Exhaust burst capacity
        await limiter.acquire(2)
        
        # Next request should wait ~0.5s for 1 token
        start = time.monotonic()
        await limiter.acquire(1)
        elapsed = time.monotonic() - start
        
        assert 0.4 < elapsed < 0.7, f"Should wait ~0.5s, waited {elapsed:.2f}s"
    
    @pytest.mark.asyncio
    async def test_concurrent_access(self):
        """Test thread safety with concurrent coroutines"""
        limiter = TokenBucketRateLimiter(rate=5.0, max_tokens=10)
        
        async def worker(worker_id):
            for _ in range(3):
                await limiter.acquire(1)
            return worker_id
        
        # Run 5 workers concurrently
        start = time.monotonic()
        results = await asyncio.gather(*[worker(i) for i in range(5)])
        elapsed = time.monotonic() - start
        
        assert len(results) == 5, "All workers completed"
        # 15 total tokens at 5/sec should take ~3s after burst
        assert elapsed < 4.0, "Concurrent access should be efficient"
    
    @pytest.mark.asyncio
    async def test_token_refill(self):
        """Test tokens refill over time"""
        limiter = TokenBucketRateLimiter(rate=10.0, max_tokens=10)
        
        # Exhaust tokens
        await limiter.acquire(10)
        assert limiter.tokens < 1
        
        # Wait for refill
        await asyncio.sleep(0.5)
        
        # Should have ~5 tokens now (10 tokens/sec * 0.5s)
        async with limiter.lock:
            now = time.monotonic()
            elapsed = now - limiter.last_update
            refilled = limiter.tokens + elapsed * limiter.rate
            assert 4 < refilled < 6, f"Expected ~5 tokens, got {refilled:.1f}"


class TestDomainRateLimiter:
    """Test domain-specific rate limiting"""
    
    @pytest.mark.asyncio
    async def test_separate_domain_limits(self):
        """Test separate limits for different domains"""
        limiter = DomainRateLimiter(default_rate=2.0)
        
        # Acquire from arxiv
        await limiter.acquire("arxiv", tokens=1)
        
        # Acquire from pubmed (should be independent)
        start = time.monotonic()
        await limiter.acquire("pubmed", tokens=1)
        elapsed = time.monotonic() - start
        
        assert elapsed < 0.1, "Different domains should be independent"
    
    @pytest.mark.asyncio
    async def test_custom_domain_rate(self):
        """Test custom rate for specific domain"""
        limiter = DomainRateLimiter(default_rate=1.0)
        
        # Set arxiv to slower rate (1/sec = 1s delay)
        await limiter.acquire("arxiv", rate=1.0)
        
        # Second request should wait ~1s
        start = time.monotonic()
        await limiter.acquire("arxiv")
        elapsed = time.monotonic() - start
        
        assert 0.8 < elapsed < 1.3, f"Should wait ~1s, waited {elapsed:.2f}s"
    
    @pytest.mark.asyncio
    async def test_get_status(self):
        """Test getting limiter status"""
        limiter = DomainRateLimiter(default_rate=5.0)
        
        # Create limiter for domain
        await limiter.acquire("test_domain", rate=5.0)
        
        # Get status
        status = limiter.get_status("test_domain")
        assert status is not None
        assert status["rate"] == 5.0
        assert status["max_tokens"] == 10  # default: rate * 2
        
        # Non-existent domain
        assert limiter.get_status("nonexistent") is None
    
    @pytest.mark.asyncio
    async def test_parallel_domains(self):
        """Test parallel requests to different domains"""
        limiter = DomainRateLimiter(default_rate=2.0)
        
        async def fetch_arxiv():
            for _ in range(3):
                await limiter.acquire("arxiv")
            return "arxiv"
        
        async def fetch_pubmed():
            for _ in range(3):
                await limiter.acquire("pubmed")
            return "pubmed"
        
        # Run in parallel
        start = time.monotonic()
        results = await asyncio.gather(fetch_arxiv(), fetch_pubmed())
        elapsed = time.monotonic() - start
        
        assert results == ["arxiv", "pubmed"]
        # Each domain does 3 requests at 2/sec independently
        # Should take ~1.5s per domain, running in parallel
        assert elapsed < 2.5, "Parallel domains should not block each other"


class TestRateLimiterEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.mark.asyncio
    async def test_zero_rate(self):
        """Test behavior with very low rate"""
        # Very low rate still works
        limiter = TokenBucketRateLimiter(rate=0.1)  # 1 token per 10 seconds
        
        await limiter.acquire(1)
        assert limiter.tokens < 1
    
    @pytest.mark.asyncio
    async def test_high_burst(self):
        """Test high burst capacity"""
        limiter = TokenBucketRateLimiter(rate=1.0, max_tokens=100)
        
        # Should allow 100 rapid requests
        start = time.monotonic()
        await limiter.acquire(100)
        elapsed = time.monotonic() - start
        
        assert elapsed < 0.5, "High burst should be fast"
    
    @pytest.mark.asyncio
    async def test_fractional_tokens(self):
        """Test fractional token rates"""
        limiter = TokenBucketRateLimiter(rate=1.0)  # 1 token per second
        
        await limiter.acquire(1)
        
        # Next should wait ~1 second
        start = time.monotonic()
        await limiter.acquire(1)
        elapsed = time.monotonic() - start
        
        assert 0.8 < elapsed < 1.3, f"Should wait ~1s, waited {elapsed:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
