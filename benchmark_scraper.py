#!/usr/bin/env python3
"""
Benchmark: Sequential vs Async Research Scraper
Compare performance and validate async speedup
"""

import asyncio
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from research_scraper_async import AsyncResearchScraper

# Import sync scraper
import importlib.util
spec = importlib.util.spec_from_file_location("sync_scraper", "5d_research_scraper.py")
sync_scraper_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_scraper_module)
ResearchScraper = sync_scraper_module.ResearchScraper


def benchmark_sync():
    """Benchmark synchronous scraper"""
    print("=" * 60)
    print("BENCHMARKING SYNCHRONOUS SCRAPER")
    print("=" * 60)
    
    scraper = ResearchScraper(rate_limit_delay=1.0)
    
    start = time.time()
    research_data = scraper.scrape_all()
    elapsed = time.time() - start
    
    total_papers = sum(
        len(data.get("arxiv", [])) + len(data.get("pubmed", [])) 
        for data in research_data.values() 
        if "arxiv" in data
    )
    
    print(f"\n{'='*60}")
    print(f"SYNC RESULTS:")
    print(f"  ⏱️  Time: {elapsed:.2f}s")
    print(f"  📄 Papers: {total_papers}")
    print(f"  ⚡ Papers/sec: {total_papers/elapsed:.2f}")
    print(f"{'='*60}\n")
    
    return {
        "time": elapsed,
        "papers": total_papers,
        "rate": total_papers/elapsed
    }


async def benchmark_async():
    """Benchmark asynchronous scraper"""
    print("=" * 60)
    print("BENCHMARKING ASYNCHRONOUS SCRAPER")
    print("=" * 60)
    
    async with AsyncResearchScraper(rate_limit_delay=1.0) as scraper:
        start = time.time()
        research_data = await scraper.scrape_all_async()
        elapsed = time.time() - start
        
        total_papers = sum(
            len(data.get("arxiv", [])) + len(data.get("pubmed", [])) 
            for data in research_data.values() 
            if "arxiv" in data
        )
        
        print(f"\n{'='*60}")
        print(f"ASYNC RESULTS:")
        print(f"  ⏱️  Time: {elapsed:.2f}s")
        print(f"  📄 Papers: {total_papers}")
        print(f"  ⚡ Papers/sec: {total_papers/elapsed:.2f}")
        print(f"{'='*60}\n")
        
        return {
            "time": elapsed,
            "papers": total_papers,
            "rate": total_papers/elapsed
        }


def print_comparison(sync_results, async_results):
    """Print comparison of results"""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    speedup = sync_results["time"] / async_results["time"]
    time_saved = sync_results["time"] - async_results["time"]
    
    print(f"\n{'Metric':<30} {'Sync':<15} {'Async':<15} {'Improvement'}")
    print("-" * 70)
    print(f"{'Time (seconds)':<30} {sync_results['time']:<15.2f} {async_results['time']:<15.2f} {speedup:.2f}x faster")
    print(f"{'Papers fetched':<30} {sync_results['papers']:<15} {async_results['papers']:<15} {'same' if sync_results['papers'] == async_results['papers'] else 'different'}")
    print(f"{'Papers/second':<30} {sync_results['rate']:<15.2f} {async_results['rate']:<15.2f} {async_results['rate']/sync_results['rate']:.2f}x")
    print(f"{'Time saved (seconds)':<30} {'-':<15} {time_saved:<15.2f} {'-'}")
    
    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)
    
    if speedup >= 5.0:
        print(f"✅ EXCELLENT: {speedup:.1f}x speedup achieved!")
        print("   Target of 5-10x speedup met!")
    elif speedup >= 3.0:
        print(f"✅ GOOD: {speedup:.1f}x speedup achieved!")
        print("   Close to target, some room for improvement.")
    elif speedup >= 2.0:
        print(f"⚠️  MODERATE: {speedup:.1f}x speedup achieved.")
        print("   Below target, investigate bottlenecks.")
    else:
        print(f"❌ POOR: Only {speedup:.1f}x speedup.")
        print("   Significant issues, review implementation.")
    
    print("=" * 60 + "\n")


async def main():
    """Run benchmarks"""
    print("\n" + "🚀" * 30)
    print("RESEARCH SCRAPER PERFORMANCE BENCHMARK")
    print("🚀" * 30 + "\n")
    
    # Run synchronous benchmark
    sync_results = benchmark_sync()
    
    # Wait a bit to avoid rate limit conflicts
    print("Waiting 5 seconds before async benchmark...\n")
    await asyncio.sleep(5)
    
    # Run asynchronous benchmark
    async_results = await benchmark_async()
    
    # Print comparison
    print_comparison(sync_results, async_results)


if __name__ == "__main__":
    asyncio.run(main())
