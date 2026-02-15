#!/usr/bin/env python3
"""
Tests for Async Research Scraper
Uses mocking to avoid network calls
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from research_scraper_async import AsyncResearchScraper


class TestAsyncResearchScraper:
    """Test async research scraper functionality"""
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager creation and cleanup"""
        scraper = AsyncResearchScraper()
        
        async with scraper as s:
            assert s.session is not None, "Session should be created"
            assert s.connector is not None, "Connector should be created"
        
        # After exit, session should be closed
        assert scraper.session.closed, "Session should be closed after exit"
    
    @pytest.mark.asyncio
    async def test_rate_limiter_initialization(self):
        """Test rate limiter is properly initialized"""
        scraper = AsyncResearchScraper(rate_limit_delay=2.0)
        
        assert scraper.rate_limiter is not None
        assert scraper.rate_limiter.default_rate == 1.0  # Domain limiter uses default
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_search_arxiv_async(self, mock_get):
        """Test arXiv search with mocked response"""
        # Mock arXiv XML response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="""
        <feed>
            <entry>
                <title>Test Paper</title>
                <author><name>Test Author</name></author>
                <summary>Test summary</summary>
                <published>2023-01-01</published>
                <id>http://arxiv.org/abs/1234.5678</id>
            </entry>
        </feed>
        """)
        mock_response.raise_for_status = MagicMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_get.return_value = mock_response
        
        async with AsyncResearchScraper() as scraper:
            papers = await scraper.search_arxiv_async("test query", max_results=1)
            
            assert len(papers) == 1
            assert papers[0]["title"] == "Test Paper"
            assert "Test Author" in papers[0]["authors"]
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_search_pubmed_async(self, mock_get):
        """Test PubMed search with mocked response"""
        # Mock PubMed search response (returns IDs)
        mock_search_response = MagicMock()
        mock_search_response.status = 200
        mock_search_response.json = AsyncMock(return_value={
            "esearchresult": {"idlist": ["12345"]}
        })
        mock_search_response.raise_for_status = MagicMock()
        mock_search_response.__aenter__ = AsyncMock(return_value=mock_search_response)
        mock_search_response.__aexit__ = AsyncMock(return_value=None)
        
        # Mock PubMed fetch response (returns paper details)
        mock_fetch_response = MagicMock()
        mock_fetch_response.status = 200
        mock_fetch_response.json = AsyncMock(return_value={
            "result": {
                "12345": {
                    "title": "Test PubMed Paper",
                    "authors": [{"name": "Dr. Test"}],
                    "pubdate": "2023"
                }
            }
        })
        mock_fetch_response.raise_for_status = MagicMock()
        mock_fetch_response.__aenter__ = AsyncMock(return_value=mock_fetch_response)
        mock_fetch_response.__aexit__ = AsyncMock(return_value=None)
        
        # Return different responses for search and fetch
        mock_get.side_effect = [mock_search_response, mock_fetch_response]
        
        async with AsyncResearchScraper() as scraper:
            papers = await scraper.search_pubmed_async("test query", max_results=1)
            
            assert len(papers) == 1
            assert papers[0]["title"] == "Test PubMed Paper"
            assert "Dr. Test" in papers[0]["authors"]
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_scrape_keyword_async(self, mock_get):
        """Test scraping a single keyword with parallel requests"""
        # Mock responses for both arXiv and PubMed
        arxiv_response = MagicMock()
        arxiv_response.status = 200
        arxiv_response.text = AsyncMock(return_value='<feed></feed>')
        arxiv_response.raise_for_status = MagicMock()
        arxiv_response.__aenter__ = AsyncMock(return_value=arxiv_response)
        arxiv_response.__aexit__ = AsyncMock(return_value=None)
        
        pubmed_search = MagicMock()
        pubmed_search.status = 200
        pubmed_search.json = AsyncMock(return_value={"esearchresult": {"idlist": []}})
        pubmed_search.raise_for_status = MagicMock()
        pubmed_search.__aenter__ = AsyncMock(return_value=pubmed_search)
        pubmed_search.__aexit__ = AsyncMock(return_value=None)
        
        mock_get.side_effect = [arxiv_response, pubmed_search]
        
        async with AsyncResearchScraper() as scraper:
            keyword, result = await scraper.scrape_keyword_async("test")
            
            assert keyword == "test"
            assert "arxiv" in result
            assert "pubmed" in result
            assert "timestamp" in result
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_rate_limit_429_handling(self, mock_get):
        """Test handling of 429 rate limit errors"""
        # First call returns 429, second succeeds
        mock_429 = MagicMock()
        mock_429.status = 429
        mock_429.__aenter__ = AsyncMock(return_value=mock_429)
        mock_429.__aexit__ = AsyncMock(return_value=None)
        
        mock_success = MagicMock()
        mock_success.status = 200
        mock_success.text = AsyncMock(return_value='<feed></feed>')
        mock_success.raise_for_status = MagicMock()
        mock_success.__aenter__ = AsyncMock(return_value=mock_success)
        mock_success.__aexit__ = AsyncMock(return_value=None)
        
        mock_get.side_effect = [mock_429, mock_success]
        
        async with AsyncResearchScraper() as scraper:
            papers = await scraper.search_arxiv_async("test", max_results=1)
            
            # Should retry and succeed
            assert isinstance(papers, list)
    
    @pytest.mark.asyncio
    async def test_parallel_keyword_scraping(self):
        """Test that multiple keywords can be scraped in parallel"""
        scraper = AsyncResearchScraper()
        # Reduce to 2 keywords for faster test
        scraper.keywords = ["autonomy", "motivation"]
        
        async with scraper as s:
            with patch('aiohttp.ClientSession.get') as mock_get:
                # Mock empty responses
                mock_response = MagicMock()
                mock_response.status = 200
                mock_response.text = AsyncMock(return_value='<feed></feed>')
                mock_response.json = AsyncMock(return_value={"esearchresult": {"idlist": []}})
                mock_response.raise_for_status = MagicMock()
                mock_response.__aenter__ = AsyncMock(return_value=mock_response)
                mock_response.__aexit__ = AsyncMock(return_value=None)
                
                mock_get.return_value = mock_response
                
                # This should execute keywords in parallel
                results = await s.scrape_all_async()
                
                # Should have results for both keywords
                assert "autonomy" in results
                assert "motivation" in results


class TestAsyncScraperPerformance:
    """Test performance characteristics of async scraper"""
    
    @pytest.mark.asyncio
    async def test_connection_pooling_configured(self):
        """Test that connection pooling is properly configured"""
        async with AsyncResearchScraper() as scraper:
            connector = scraper.connector
            
            # Check connection limits
            assert connector._limit == 10, "Should have max 10 concurrent connections"
            assert connector._limit_per_host == 5, "Should have max 5 connections per host"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
