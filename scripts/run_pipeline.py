"""
Main Pipeline Runner for JoBSearchAntigravity
Executes Discovery -> Matching -> Drafting in one end-to-end command.
"""

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from search_and_extract import discover_postings
from dossier_engine import run_dossier_engine

def run():
    print("=" * 65)
    print("      JoBSearchAntigravity - Dossier-Grade Job Hunter & Drafter      ")
    print("=" * 65)
    start_time = time.time()
    
    # 1. Discover jobs via Firecrawl
    print("\n[Step 1/2] Discovering target company job postings...")
    discover_postings(limit_per_query=2)
    
    # 2. Match, Fact-Guard, and Compile LaTeX PDFs
    print("\n[Step 2/2] Running Dossier-Grade Matcher, Fact Guard & LaTeX Compiler...")
    drafted = run_dossier_engine()
    
    duration = round(time.time() - start_time, 2)
    print("\n" + "=" * 65)
    print(f"Pipeline completed in {duration} seconds.")
    if drafted:
        print(f"Compiled {len(drafted)} application packets (PDFs + LaTeX + Fact Guard):")
        for app in drafted:
            print(f" -> applications/{app}")
    else:
        print("No new jobs met the match threshold today. Tracker is up to date.")
    print("=" * 65)

if __name__ == "__main__":
    run()
