"""
Job Search and Discovery Module — Strict ATS Deep-Linking & Multi-Portal Feeds
Connects FreeHire (direct career pages, Workday, Greenhouse, Lever, LinkedIn),
JSearch (OpenWeb Ninja / RapidAPI), and Firecrawl ATS deep-link search.
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from job_portals import discover_all_niche_jobs, is_direct_job_link
from firecrawl_client import search_jobs, scrape_url, load_api_key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
SEEN_JOBS_PATH = os.path.join(BASE_DIR, "tracker", "seen_jobs.json")
DISCOVERED_DIR = os.path.join(BASE_DIR, "data", "discovered")

os.makedirs(DISCOVERED_DIR, exist_ok=True)

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_seen():
    if os.path.exists(SEEN_JOBS_PATH):
        try:
            with open(SEEN_JOBS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"seen_urls": [], "seen_ids": []}

def save_seen(seen_data):
    with open(SEEN_JOBS_PATH, "w", encoding="utf-8") as f:
        json.dump(seen_data, f, indent=2)

def discover_postings(limit_per_query: int = 3):
    cfg = load_config()
    seen = load_seen()
    seen_urls = set(seen.get("seen_urls", []))
    discovered = []
    
    print("=== Step 1: Querying Niche ATS Portals (FreeHire & JSearch) ===")
    niche_jobs = discover_all_niche_jobs(country="in", limit_per_source=limit_per_query)
    
    for job in niche_jobs:
        url = job.get("url", "")
        if not url or url in seen_urls:
            continue
            
        if not is_direct_job_link(url):
            print(f"  [-] Skipping non-direct job link: {url}")
            continue
            
        company = job.get("company", "Company")
        role = job.get("title", "Embedded Engineer")
        clean_company = re.sub(r'[^a-zA-Z0-9]', '_', company)[:20]
        clean_role = re.sub(r'[^a-zA-Z0-9]', '_', role)[:25]
        
        job_entry = {
            "id": f"{clean_company}_{clean_role}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "company": company,
            "role": role,
            "location": job.get("location", "India"),
            "title": f"{role} at {company}",
            "url": url,
            "portal": job.get("portal", "FreeHire"),
            "discovered_at": datetime.now().isoformat(),
            "markdown": job.get("description", "")
        }
        
        filepath = os.path.join(DISCOVERED_DIR, f"{job_entry['id']}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(job_entry, f, indent=2)
            
        discovered.append(job_entry)
        seen_urls.add(url)
        print(f"  [+] Saved Niche ATS Requisition: {job_entry['title']} -> {url}")
        
    print(f"\n=== Step 2: Querying Corporate ATS Requisitions via Firecrawl ===")
    targeted_queries = [
        {"company": "Rockwell Automation", "role": "Firmware Engineer", "q": "site:rockwellautomation.wd1.myworkdayjobs.com/External_Rockwell_Automation/job/ Firmware"},
        {"company": "Schneider Electric", "role": "Embedded Software Designer", "q": "site:careers.se.com inurl:jobs embedded"},
        {"company": "Schneider Electric", "role": "R&D Embedded Systems Engineer", "q": "site:careers.se.com inurl:jobs firmware"},
        {"company": "Siemens", "role": "Embedded Software Developer", "q": "site:jobs.siemens.com/en_US/externaljobs/JobDetail embedded"}
    ]
    
    for item in targeted_queries:
        company = item["company"]
        role = item["role"]
        query = item["q"]
        print(f"Searching ATS: '{query}'...")
        try:
            results = search_jobs(query, limit=2)
            for res in results:
                url = res.get("url", "")
                title = res.get("title", f"{role} at {company}")
                markdown = res.get("markdown", "")
                
                if not url or url in seen_urls:
                    continue
                    
                if not is_direct_job_link(url):
                    print(f"  [-] Rejected non-direct URL: {url[:70]}...")
                    continue
                    
                clean_title = title.split("|")[0].split(" - Job Detail")[0].strip()
                clean_company = re.sub(r'[^a-zA-Z0-9]', '_', company)[:20]
                clean_role = re.sub(r'[^a-zA-Z0-9]', '_', role)[:25]
                
                job_entry = {
                    "id": f"{clean_company}_{clean_role}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "company": company,
                    "role": role,
                    "location": "India / Remote / Hybrid",
                    "title": clean_title,
                    "url": url,
                    "portal": "Firecrawl ATS",
                    "discovered_at": datetime.now().isoformat(),
                    "markdown": markdown[:20000]
                }
                
                filepath = os.path.join(DISCOVERED_DIR, f"{job_entry['id']}.json")
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(job_entry, f, indent=2)
                    
                discovered.append(job_entry)
                seen_urls.add(url)
                print(f"  [+] Saved Verified ATS Requisition: {clean_title} -> {url}")
            time.sleep(1.5)
        except Exception as e:
            print(f"  [!] Search error for {company}: {e}")
            
    seen["seen_urls"] = list(seen_urls)
    save_seen(seen)
    print(f"\nDiscovery complete! Found {len(discovered)} direct-apply corporate job requisitions.")
    return discovered

if __name__ == "__main__":
    discover_postings(limit_per_query=2)
