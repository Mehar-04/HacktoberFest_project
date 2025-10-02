import asyncio
import aiohttp
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

# Caching function for expensive computations
@lru_cache(maxsize=1000)
def expensive_computation(x: int) -> int:
    # Simulates a CPU-heavy task
    total = 0
    for i in range(1, 10**5):
        total += (x * i) % 97
    return total

async def fetch(session: aiohttp.ClientSession, url: str, retries: int = 3) -> str:
    """Fetch URL with retry logic"""
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # exponential backoff
            else:
                return f"Failed to fetch {url}: {e}"

async def scrape_all(urls: list[str]) -> dict[str, str]:
    """Scrape multiple URLs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return dict(zip(urls, responses))

def run_computations(numbers: list[int]) -> dict[int, int]:
    """Run CPU-bound computations in a thread pool"""
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(expensive_computation, numbers))
    return dict(zip(numbers, results))

async def main():
    start = time.time()

    urls = [
        "https://httpbin.org/get",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
    ]
    numbers = [42, 1337, 2025, 99999]

    # Run async scraping + threaded computations concurrently
    scrape_task = asyncio.create_task(scrape_all(urls))
    loop = asyncio.get_event_loop()
    comp_task = loop.run_in_executor(None, run_computations, numbers)

    scraped, computed = await asyncio.gather(scrape_task, comp_task)

    print("\n--- Web Scraping Results ---")
    for url, data in scraped.items():
        print(f"{url[:40]}: {data[:60]}...\n")

    print("\n--- Computation Results ---")
    for n, result in computed.items():
        print(f"{n} -> {result}")

    print(f"\nTotal time: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
