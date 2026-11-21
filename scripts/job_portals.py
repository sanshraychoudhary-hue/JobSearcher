"""
Multi-Portal Job Discovery Engine
Connects to authentic ATS and job search providers:
1. FreeHire API (Free, zero-key, direct Workday/Greenhouse/Lever/LinkedIn job feeds)
2. OpenWeb Ninja / JSearch (RapidAPI / OpenWeb Ninja API for LinkedIn, Indeed, Google for Jobs)
3. Direct Corporate ATS scrapers with strict individual requisition deep-linking
"""

import os
import re
import json
import urllib.request
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def load_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def strip_html(html_text: str) -> str:
    """Cleans raw HTML into readable plain text / markdown."""
    if not html_text:
        return ""
    # Replace breaks and paragraphs with newlines
    text = re.sub(r'<br\s*/?>', '\n', html_text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<li>', '\n• ', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    lines = [line.strip() for line in text.splitlines()]
    return '\n'.join(line for line in lines if line)

def is_direct_job_link(url: str) -> bool:
    """
    Validates that a URL points to a specific, apply-ready job opening,
    and NOT a general career home page or search results directory.
    """
    if not url or not url.startswith("http"):
        return False
        
    url_lower = url.lower()
    
    # Generic portals to reject
    generic_blocks = [
        "/overview", "/all-jobs", "/all_jobs", "/category", "/categories",
        "/blogs/", "quora.com", "reddit.com", "medium.com", "youtube.com",
        "/search-results", "/search?", "srsltid=", "/how-to-",
        "/sites/honeywell/jobs", # Generic honeywell search page
        "careers.se.com/jobs?",   # Generic schneider search page without id
        "jobs.siemens.com/jobs?",
        "jobs.sw.siemens.com/remotehybridonsite/remote/jobs/"
    ]
    for b in generic_blocks:
        if b in url_lower:
            return False
            
    # Valid direct patterns
    valid_patterns = [
        r'linkedin\.com/jobs/view/\d+',
        r'myworkdayjobs\.com/.+/job/.+',
        r'boards\.greenhouse\.io/[^/]+/\d+',
        r'jobs\.lever\.co/[^/]+/[a-f0-9-]+',
        r'freshteam\.com/jobs/[^/]+/.+',
        r'zohorecruit\.in/jobs/careers/\d+',
        r'smartrecruiters\.com/[^/]+/\d+',
        r'oraclecloud\.com/.+/job/\d+',
        r'careers\.se\.com/.*jobs/\d+',
        r'jobs\.siemens\.com/.*(?:JobDetail|job)/\d+',
        r'careers\.honeywell\.com/.*job/\d+',
        r'corporate\..+\?position=.+',
        r'hirist\.tech/j/.+-\d+',
        r'shine\.com/jobs/.+/\d+'
    ]
    for pat in valid_patterns:
        if re.search(pat, url_lower):
            return True
            
    # Fallback: ends with numeric ID or slug with ID
    if re.search(r'/\d{4,}', url) or re.search(r'jobid=\d+', url_lower) or re.search(r'reqid=\d+', url_lower):
        return True
        
    return False

class FreeHirePortal:
    """
    Queries FreeHire API (https://freehire.me).
    Zero API key required. High-quality tech postings directly from company career pages.
    """
    BASE_URL = "https://freehire.me/api/v1/agent/jobs/search"
    
    def search(self, keywords: str, country: str = "in", limit: int = 10) -> List[Dict[str, Any]]:
        params = {
            "q": keywords,
            "countries": country.upper(),
            "limit": limit,
            "description_format": "text"
        }
        query_str = urllib.parse.urlencode(params)
        url = f"{self.BASE_URL}?{query_str}"
        req = urllib.request.Request(url, headers={"User-Agent": "Dossier/1.0", "Accept": "application/json"})
        
        postings = []
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                items = data.get("data", [])
                for item in items:
                    job_url = item.get("url") or f"https://freehire.me/jobs/{item.get('public_slug')}"
                    desc = item.get("description", "")
                    if "<" in desc and ">" in desc:
                        desc = strip_html(desc)
                        
                    postings.append({
                        "portal": "FreeHire",
                        "id": str(item.get("external_id") or item.get("public_slug")),
                        "title": item.get("title", "Embedded Engineer"),
                        "company": item.get("company", "Company"),
                        "location": item.get("location", "India"),
                        "url": job_url,
                        "description": desc,
                        "posted_at": item.get("posted_at") or datetime.now().isoformat(),
                        "is_direct": is_direct_job_link(job_url)
                    })
        except Exception as e:
            print(f"[FreeHire] Search failed for '{keywords}': {e}")
            
        return postings

class JSearchPortal:
    """
    Queries JSearch API (OpenWeb Ninja or RapidAPI).
    Requires 'jsearch_api_key' in config.json.
    """
    def __init__(self, api_key: Optional[str] = None, host: str = "openwebninja"):
        self.api_key = api_key
        self.host = host # 'openwebninja' or 'rapidapi'
        
    def search(self, keywords: str, country: str = "in", limit: int = 10) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []
            
        if self.host == "rapidapi":
            base_url = "https://jsearch.p.rapidapi.com/search-v2"
            headers = {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": "jsearch.p.rapidapi.com"
            }
        else:
            base_url = "https://api.openwebninja.com/jsearch/search-v2"
            headers = {
                "x-api-key": self.api_key
            }
            
        params = {
            "query": f"{keywords} in India" if country.lower() == "in" else keywords,
            "country": country.lower(),
            "date_posted": "week",
            "num_pages": 1
        }
        query_str = urllib.parse.urlencode(params)
        url = f"{base_url}?{query_str}"
        req = urllib.request.Request(url, headers=headers)
        
        postings = []
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                items = data.get("data", [])
                for item in items:
                    job_url = item.get("job_apply_link") or item.get("job_google_link") or "#"
                    city = item.get("job_city", "")
                    country_name = item.get("job_country", "")
                    loc = f"{city}, {country_name}".strip(", ") if city else country_name
                    
                    postings.append({
                        "portal": "JSearch",
                        "id": str(item.get("job_id", "")),
                        "title": item.get("job_title", "Engineer"),
                        "company": item.get("employer_name", "Company"),
                        "location": loc or "India",
                        "url": job_url,
                        "description": item.get("job_description", ""),
                        "posted_at": item.get("job_posted_at_datetime_utc") or datetime.now().isoformat(),
                        "is_direct": is_direct_job_link(job_url)
                    })
        except Exception as e:
            print(f"[JSearch] Search failed for '{keywords}': {e}")
            
        return postings

def discover_all_niche_jobs(country: str = "in", limit_per_source: int = 4) -> List[Dict[str, Any]]:
    """
    Orchestrates job discovery across all available niche portals:
    FreeHire + OpenWeb Ninja / JSearch.
    """
    cfg = load_config()
    jsearch_key = cfg.get("jsearch_api_key", "")
    
    freehire = FreeHirePortal()
    jsearch = JSearchPortal(api_key=jsearch_key if jsearch_key else None)
    
    # Specific search targets tailored to Sanshray (Undergrad 2027, Intern/Fresher/Junior, India & Remote)
    targets = [
        {"q": "Embedded Intern", "country": "in", "remote": False},
        {"q": "Firmware Intern", "country": "in", "remote": False},
        {"q": "Robotics Intern", "country": "in", "remote": False},
        {"q": "Robotics ROS 2", "country": "in", "remote": False},
        {"q": "Junior Embedded Engineer", "country": "in", "remote": False},
        {"q": "Associate Firmware Engineer", "country": "in", "remote": False},
        {"q": "Embedded Engineer Fresher", "country": "in", "remote": False},
        {"q": "Rockwell Automation Firmware", "country": "in", "remote": False},
        {"q": "Schneider Electric Embedded", "country": "in", "remote": False},
        {"q": "Embedded Software", "country": "", "remote": True}, # Remote global
        {"q": "Firmware Engineer", "country": "", "remote": True}  # Remote global
    ]
    
    all_jobs = []
    seen_urls = set()
    
    for item in targets:
        q = item["q"]
        cntry = item["country"]
        is_rem = item["remote"]
        tag = f"Remote" if is_rem else f"India ({cntry})"
        print(f"Querying niche ATS portals for: '{q}' [{tag}]...")
        
        # 1. FreeHire (Primary, free, 100% authentic)
        fh_results = freehire.search(q, country=cntry or "in", limit=limit_per_source)
        for job in fh_results:
            u = job.get("url")
            if u and u not in seen_urls and job.get("is_direct", False):
                seen_urls.add(u)
                all_jobs.append(job)
                
        # 2. JSearch (if key configured)
        if jsearch_key:
            js_results = jsearch.search(q, country=cntry or "in", limit=limit_per_source)
            for job in js_results:
                u = job.get("url")
                if u and u not in seen_urls and job.get("is_direct", False):
                    seen_urls.add(u)
                    all_jobs.append(job)
                    
    print(f"[Portals] Discovered {len(all_jobs)} verified, direct-apply job postings.")
    return all_jobs

if __name__ == "__main__":
    jobs = discover_all_niche_jobs(country="in", limit_per_source=2)
    for j in jobs[:5]:
        print(f"- [{j['portal']}] {j['title']} at {j['company']} ({j['location']})")
        print(f"  Direct Link: {j['url']}")
