#!/usr/bin/env python3
"""
Token Bucket Rate Limiter for Async API Calls
Implements fair rate limiting with burst capacity
"""

import asyncio
import time


class TokenBucketRateLimiter:
    """
    Async token bucket rate limiter for API calls.
    
    Allows bursts up to max_tokens while maintaining average rate.
    Thread-safe for concurrent async operations.
    
    Reference: Token bucket algorithm (Tanenbaum, Computer Networks)
    """
    
    def __init__(self, rate: float, max_tokens: int | None = None):
        """
        Initialize rate limiter.
        
        Args:
            rate: Tokens per second (e.g., 1.0 = 1 request/sec)
            max_tokens: Maximum burst capacity (default: rate * 2)
        """
        self.rate = rate
        self.max_tokens = max_tokens or int(rate * 2)
        self.tokens = float(self.max_tokens)
        self.last_update = time.monotonic()
        self.lock = asyncio.Lock()
        
    async def acquire(self, tokens: int = 1) -> None:
        """
        Acquire tokens (wait if necessary).
        
        Args:
            tokens: Number of tokens to acquire (default: 1)
        """
        async with self.lock:
            while True:
                now = time.monotonic()
                elapsed = now - self.last_update
                
                # Refill tokens based on elapsed time
                self.tokens = min(
                    self.max_tokens,
                    self.tokens + elapsed * self.rate
                )
                self.last_update = now
                
                # If we have enough tokens, consume and return
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return
                
                # Calculate wait time for required tokens
                needed = tokens - self.tokens
                wait_time = needed / self.rate
                
                # Release lock during sleep to allow other coroutines
                await asyncio.sleep(wait_time)


class DomainRateLimiter:
    """
    Multi-domain rate limiter with separate buckets per domain.
    
    Useful for managing rate limits across different API endpoints.
    """
    
    def __init__(self, default_rate: float = 1.0):
        """
        Initialize domain rate limiter.
        
        Args:
            default_rate: Default tokens per second for new domains
        """
        self.default_rate = default_rate
        self.limiters: dict[str, TokenBucketRateLimiter] = {}
        self.lock = asyncio.Lock()
        
    async def acquire(self, domain: str, tokens: int = 1, rate: float | None = None) -> None:
        """
        Acquire tokens for a specific domain.
        
        Args:
            domain: Domain identifier (e.g., "arxiv", "pubmed")
            tokens: Number of tokens to acquire
            rate: Override rate for this domain (tokens per second)
        """
        # Get or create limiter for this domain
        async with self.lock:
            if domain not in self.limiters:
                domain_rate = rate or self.default_rate
                self.limiters[domain] = TokenBucketRateLimiter(domain_rate)
        
        # Acquire tokens from domain-specific limiter
        await self.limiters[domain].acquire(tokens)
    
    def get_status(self, domain: str) -> dict[str, float] | None:
        """
        Get current status of a domain's rate limiter.
        
        Args:
            domain: Domain identifier
            
        Returns:
            Dict with tokens, rate, max_tokens or None if domain not found
        """
        limiter = self.limiters.get(domain)
        if limiter:
            return {
                "tokens": limiter.tokens,
                "rate": limiter.rate,
                "max_tokens": limiter.max_tokens
            }
        return None
