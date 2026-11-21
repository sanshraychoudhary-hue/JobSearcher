"""
Firecrawl Client
Provides zero-dependency Python methods to scrape and search using Firecrawl API v1.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

def load_api_key() -> str:
    """Loads the Firecrawl API key from config.json or environment."""
    env_key = os.environ.get("FIRECRAWL_API_KEY")
    if env_key:
        return env_key
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                key = cfg.get("firecrawl_api_key")
                if key and not key.startswith("fc-your"):
                    return key
        except Exception:
            pass
    raise ValueError("FIRECRAWL_API_KEY not found in environment or config.json.")

def _post_json(url: str, payload: Dict[str, Any], api_key: str, timeout: int = 45, max_retries: int = 3) -> Dict[str, Any]:
    """Sends a JSON POST request with Bearer authorization and handles rate limits."""
    import time
    data = json.dumps(payload).encode("utf-8")
    
    for attempt in range(max_retries):
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "AntigravityJobHunter/1.0"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            if e.code == 429 and attempt < max_retries - 1:
                # Try to parse retry_after_seconds
                wait_sec = 8
                try:
                    err_json = json.loads(err_msg)
                    wait_sec = err_json.get("retry_after_seconds", 8) + 1
                except Exception:
                    pass
                print(f"    [i] Rate limit hit. Waiting {wait_sec}s before retry...")
                time.sleep(wait_sec)
                continue
            raise RuntimeError(f"Firecrawl API Error ({e.code}): {err_msg}")
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise RuntimeError(f"Request failed: {str(e)}")
    raise RuntimeError("Max retries exceeded.")

def scrape_url(url: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Scrapes a single URL and returns clean Markdown and metadata.
    """
    key = api_key or load_api_key()
    api_url = "https://api.firecrawl.dev/v1/scrape"
    payload = {
        "url": url,
        "formats": ["markdown"]
    }
    result = _post_json(api_url, payload, key)
    if not result.get("success"):
        raise RuntimeError(f"Firecrawl scrape failed: {result}")
    
    data = result.get("data", {})
    return {
        "url": url,
        "markdown": data.get("markdown", ""),
        "metadata": data.get("metadata", {})
    }

def search_jobs(query: str, limit: int = 5, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Searches the web via Firecrawl and returns markdown content for matching pages.
    """
    key = api_key or load_api_key()
    api_url = "https://api.firecrawl.dev/v1/search"
    payload = {
        "query": query,
        "limit": limit,
        "scrapeOptions": {
            "formats": ["markdown"]
        }
    }
    result = _post_json(api_url, payload, key)
    if not result.get("success"):
        raise RuntimeError(f"Firecrawl search failed: {result}")
    
    return result.get("data", [])

if __name__ == "__main__":
    print("Testing Firecrawl client...")
    try:
        k = load_api_key()
        print(f"API key loaded: {k[:6]}...{k[-4:]}")
        test_url = "https://example.com"
        res = scrape_url(test_url, k)
        print("Scrape test successful! Title:", res.get("metadata", {}).get("title"))
    except Exception as e:
        print("Test error:", e)
        sys.exit(1)
