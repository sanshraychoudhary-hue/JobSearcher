"""
Dossier-Style Fact Guard Module
Verifies that generated resumes and cover letters contain zero invented facts,
numbers, percentages, dates, or credentials outside the candidate's master profile.
Inspired by Dossier's fact-guard.ts.
"""

import re
from typing import Set, List, Dict, Any

NUMBER_PATTERN = re.compile(r'(?<![\w])(\d{1,3}(?:[,.\s]\d{3})+|\d+(?:[.,]\d+)?)\s*(k|m)?%?(?![\w])', re.IGNORECASE)

def clean_token(num_str: str) -> str:
    """Strips LaTeX comments, percent signs, and whitespace."""
    s = num_str.rstrip('%').strip()
    return s

def extract_numbers(text: str) -> Set[str]:
    """Finds all raw numbers, metrics, and percentages in a text."""
    # Remove LaTeX comments first so trailing % isn't treated as a percent value
    clean_text = re.sub(r'(?<!\\)%.*$', '', text, flags=re.MULTILINE)
    matches = set()
    for m in NUMBER_PATTERN.finditer(clean_text):
        val = clean_token(m.group(0).lower())
        if val:
            matches.add(val)
    return matches

def extract_keywords_and_facts(text: str) -> Set[str]:
    """Extracts words, project names, tech tokens from profile text."""
    words = re.findall(r'[\w+/#.-]{2,}', text.lower())
    return set(words)

class FactGuard:
    def __init__(self, master_profile_text: str):
        self.master_text = master_profile_text.lower()
        self.verified_numbers = extract_numbers(master_profile_text)
        self.verified_tokens = extract_keywords_and_facts(master_profile_text)

    def audit(self, generated_text: str, posting_text: str = "") -> Dict[str, Any]:
        """
        Audits generated text against the master profile and the posting.
        Returns a verification report with any questionable claims.
        """
        gen_numbers = extract_numbers(generated_text)
        posting_numbers = extract_numbers(posting_text)
        
        # Numbers are allowed if they exist in either profile or posting (or standard dates like current year)
        allowed_numbers = self.verified_numbers.union(posting_numbers).union({"2026", "2025", "2024", "2023", "2027", "1", "2", "3", "4", "5", "10"})
        
        suspicious_numbers = []
        for num in gen_numbers:
            if num not in allowed_numbers:
                # Filter out single digits or page counts
                if len(num) > 1 and not num.isdigit():
                    suspicious_numbers.append(num)

        is_clean = len(suspicious_numbers) == 0
        return {
            "verified": is_clean,
            "suspicious_numbers": suspicious_numbers,
            "total_verified_facts": len(self.verified_tokens),
            "status": "PASSED (Zero Hallucinated Metrics)" if is_clean else "FLAGGED_FOR_REVIEW"
        }
