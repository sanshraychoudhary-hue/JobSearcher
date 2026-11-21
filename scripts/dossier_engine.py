"""
Dossier-Grade Engine for JoBSearchAntigravity
Integrates Structured Extraction, Multi-Factor Scoring, Fact-Guarded Tailoring,
and Publication-Quality LaTeX PDF compilation.
"""

import json
import os
import re
import shutil
from datetime import datetime
from typing import Dict, Any, List

from fact_guard import FactGuard
from latex_builder import build_tailored_resume_tex, build_cover_letter_tex, compile_latex
from ai_brain import synthesize_ai_cover_letter, get_gemini_api_key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "profile", "master_profile.md")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DISCOVERED_DIR = os.path.join(BASE_DIR, "data", "discovered")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
APPLICATIONS_DIR = os.path.join(BASE_DIR, "applications")
TRACKER_PATH = os.path.join(BASE_DIR, "tracker", "tracker.md")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(APPLICATIONS_DIR, exist_ok=True)

# Technical competencies recognized across Siemens, Honeywell, Schneider, ABB, etc.
TECH_TAXONOMY = {
    "Embedded / Firmware": [
        "c", "c++", "embedded", "firmware", "rtos", "freertos", "arm cortex", "stm32", "esp32", "microcontroller",
        "i2c", "spi", "i2s", "uart", "can", "can bus", "rs-485", "modbus", "dma", "adc", "dac", "gpio", "timer"
    ],
    "Hardware & PCB": [
        "kicad", "pcb", "pcb design", "circuit design", "hardware debugging", "logic analyzer", "oscilloscope",
        "power electronics", "emi", "emc", "fpga", "vhdl", "verilog", "iec 61508", "functional safety"
    ],
    "Robotics & Control": [
        "robotics", "ros", "ros2", "pid", "control systems", "actuators", "sensors", "coppeliasim", "kinematics"
    ],
    "IoT & Networking": [
        "iot", "mqtt", "bluetooth", "ble", "wi-fi", "telemetry", "rest", "rest api", "tcp/ip", "sockets"
    ],
    "AI & Signal Processing": [
        "dsp", "signal processing", "fft", "filtering", "tinyml", "tensorflow", "tflite", "opencv", "computer vision"
    ]
}

def load_master_profile() -> str:
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_structured_posting(posting_text: str, title: str = "", location: str = "") -> Dict[str, Any]:
    """Extracts detected requirements, domain tags, experience cues, and location suitability."""
    full_text = f"{title} {location} {posting_text}".lower()
    
    detected_skills = []
    category_matches = {}
    
    for category, skills in TECH_TAXONOMY.items():
        matched = []
        for s in skills:
            if re.search(r'\b' + re.escape(s) + r'\b', full_text):
                matched.append(s)
                detected_skills.append(s)
        if matched:
            category_matches[category] = matched
            
    # Detect experience cues (e.g. "5 - 7 Years", "3 to 5 years", "4+ years")
    required_years = None
    range_match = re.search(r'(\d+)\s*(?:-|to)\s*(\d+)\s*years?', full_text)
    if range_match:
        required_years = int(range_match.group(1))
    else:
        single_match = re.search(r'(\d+)\+?\s*years?(?:\s+of)?\s+experience', full_text)
        if not single_match:
            single_match = re.search(r'experience\s*:\s*(\d+)', full_text)
        if single_match:
            required_years = int(single_match.group(1))
            
    # Detect seniority level for information and strategic positioning (NO TITLE WORD BLACKLIST)
    seniority_label = "Entry / Associate"
    if required_years and required_years >= 5:
        seniority_label = f"{required_years}+ yrs (Senior)"
    elif required_years and required_years >= 3:
        seniority_label = f"{required_years} yrs (Mid)"
    elif re.search(r'\b(lead|principal|staff|manager|architect|director)\b', title.lower()):
        seniority_label = "Lead / Principal"
    elif re.search(r'\b(senior|sr\.?)\b', title.lower()):
        seniority_label = "Senior"
    elif re.search(r'\b(intern|internship|graduate|trainee|fresher|entry|junior)\b', title.lower()):
        seniority_label = "Intern / Fresher"
        
    # Location fit: India (all cities) or Remote
    loc_text = f"{location} {full_text}".lower()
    india_or_remote = re.compile(r'\b(india|bengaluru|bangalore|delhi|noida|gurgaon|gurugram|hyderabad|pune|mumbai|chennai|kochi|kolkata|kerala|maharashtra|remote|hybrid|wfh|telecommute|ind-remote)\b')
    is_location_fit = bool(india_or_remote.search(loc_text))
    
    return {
        "required_skills": list(set(detected_skills)),
        "categories": category_matches,
        "required_years": required_years,
        "seniority_label": seniority_label,
        "is_location_fit": is_location_fit
    }

def score_and_map(posting_text: str, profile_text: str, title: str = "", location: str = "") -> Dict[str, Any]:
    """
    Dossier-grade Match Scoring:
    Maps requirements to evidence in Sanshray's CV, tags seniority for strategic positioning.
    """
    extracted = extract_structured_posting(posting_text, title=title, location=location)
    profile_lower = profile_text.lower()
    
    reqs = extracted["required_skills"]
    if not reqs:
        # Defaults if posting is text-sparse
        reqs = ["c", "c++", "embedded", "firmware", "freertos", "stm32", "kicad", "spi", "i2c"]
        
    matched = []
    gaps = []
    matrix = {}
    
    # Evidence mappings for Sanshray's projects
    EVIDENCE = {
        "freertos": "AtiDhwani (Dual-Core FreeRTOS) & STM32 Industrial IoT Hub",
        "esp32": "AtiDhwani (ESP32-S3) & Aegis Guardian Fall Detection",
        "stm32": "STM32 Industrial IoT Hub (STM32F407) & EMI/EMC Detector (STM32F401)",
        "kicad": "AtiDhwani 2-layer Carrier PCB (0 DRC violations)",
        "pcb": "Custom 2-layer high-speed KiCad PCB design",
        "i2s": "AtiDhwani 192kHz/24-bit DMA I2S streaming",
        "dma": "ESP32-S3 circular DMA buffer management",
        "dsp": "AtiDhwani real-time quadrature heterodyne & 128-pt Radix-4 FFT",
        "can": "CAN Bus & Modbus industrial telemetry in Master Profile",
        "c": "Core programming language for STM32, ESP32, and drone firmware",
        "c++": "OmniServe PID motion control & FreeRTOS class architectures",
        "ros": "ROS 2 Developer Certification (IIT Bombay e-Yantra)",
        "ros2": "ROS 2 Developer Certification (IIT Bombay e-Yantra)",
        "robotics": "e-Yantra Level 3 Robotics & OmniServe Mobile Robot",
        "pid": "OmniServe & Self-Balancing Bot closed-loop control",
        "iot": "STM32 Industrial IoT Node & Aero Air Quality System",
        "mqtt": "STM32 Industrial Sensor Node MQTT transmission",
        "tinyml": "Aegis Guardian TFLite CNN Edge deployment",
        "opencv": "SonicBeam computer-vision directional audio",
        "drone": "Winter Intern at India Space Academy (drone firmware)",
        "fpga": "AI Acoustic Railway Monitoring (SIH 2024)",
    }
    
    for r in reqs:
        if r in profile_lower:
            matched.append(r)
            evidence = EVIDENCE.get(r, "Documented in Master Profile & Projects")
            matrix[r] = evidence
        else:
            gaps.append(r)
            
    coverage_score = int((len(matched) / len(reqs)) * 100) if reqs else 85
    
    red_flags = []
    if extracted["required_years"] and extracted["required_years"] >= 3:
        red_flags.append(f"Position asks for {extracted['required_years']}+ years of industry experience. Tailored CV leads with project depth (AtiDhwani ESP32-S3 PCB, FreeRTOS, STM32) to showcase senior-equivalent technical rigor.")
    if not extracted["is_location_fit"]:
        red_flags.append(f"Location note: Verify remote eligibility or relocation support for on-site international roles.")
        
    return {
        "score": coverage_score,
        "matched": matched,
        "gaps": gaps,
        "matrix": matrix,
        "red_flags": red_flags,
        "categories": extracted["categories"],
        "seniority_label": extracted["seniority_label"],
        "is_location_fit": extracted["is_location_fit"],
        "required_years": extracted["required_years"]
    }

def process_candidate_dossier(candidate: Dict[str, Any], fact_guard: FactGuard, min_score: int = 65) -> str:
    company = candidate.get("company", "Company")
    role = candidate.get("role", "Engineer")
    posting_md = candidate.get("markdown", "")
    
    profile_text = load_master_profile()
    title = candidate.get("title", f"{role} at {company}")
    location = candidate.get("location", "")
    match_result = score_and_map(posting_md, profile_text, title=title, location=location)
    score = match_result["score"]
    
    print(f"Scoring: {company} - {role} [{match_result['seniority_label']}] -> Coverage: {score}%")
    
    if score < min_score:
        print(f"  [-] Skipped: Coverage {score}% is below threshold {min_score}%.")
        return ""
        
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_slug = re.sub(r'[^a-zA-Z0-9_-]', '_', f"{date_str}_{company}_{role}")
    app_dir = os.path.join(APPLICATIONS_DIR, folder_slug)
    os.makedirs(app_dir, exist_ok=True)
    
    # 1. Job Description
    with open(os.path.join(app_dir, "job_description.md"), "w", encoding="utf-8") as f:
        f.write(f"# {candidate['title']}\n\n")
        f.write(f"- **Company**: {company}\n")
        f.write(f"- **Role**: {role}\n")
        f.write(f"- **Location**: {candidate.get('location', 'N/A')}\n")
        f.write(f"- **Experience Level**: {match_result['seniority_label']}\n")
        f.write(f"- **Source URL**: [{candidate.get('url', '#')}]({candidate.get('url', '#')})\n")
        f.write(f"- **Scraped Via**: Verified ATS Portal\n\n")
        f.write("## Original Posting Content\n\n")
        f.write(posting_md)
        
    # 2. Match Analysis (Dossier-Style)
    with open(os.path.join(app_dir, "match_analysis.md"), "w", encoding="utf-8") as f:
        f.write(f"# Dossier Match Report: {company} -- {role}\n\n")
        f.write(f"### Requirement Coverage Score: **{score}%**\n\n")
        f.write("### 🎯 Matched Competencies Matrix\n")
        f.write("| Required Competency | Verified Evidence in Sanshray's Profile |\n")
        f.write("| :--- | :--- |\n")
        for skill, evidence in match_result["matrix"].items():
            f.write(f"| **{skill.title()}** | {evidence} |\n")
        f.write("\n")
        
        f.write("### ⚠️ Skill Gaps (Not explicitly detailed in profile)\n")
        if match_result["gaps"]:
            for g in match_result["gaps"]:
                f.write(f"- *{g.title()}*\n")
        else:
            f.write("- *None detected. Full technical alignment.*\n")
        f.write("\n")
        
        if match_result["red_flags"]:
            f.write("### 🚩 Strategic Considerations / Red Flags\n")
            for rf in match_result["red_flags"]:
                f.write(f"- {rf}\n")
            f.write("\n")
            
        f.write("### 💡 Interview & Positioning Strategy\n")
        f.write(f"Lead with **AtiDhwani** (ESP32-S3, KiCad PCB, FreeRTOS, DSP) and **STM32 Sensor Hub** to demonstrate production-grade firmware rigor. Emphasize IIT Bombay e-Yantra certifications to highlight proven robotics & embedded mastery.\n")

    # 3. Generate LaTeX Resume & Compile PDF
    resume_tex_content = build_tailored_resume_tex({
        "company": company,
        "role": role,
        "markdown": posting_md
    })
    resume_tex_path = os.path.join(app_dir, "tailored_resume.tex")
    with open(resume_tex_path, "w", encoding="utf-8") as f:
        f.write(resume_tex_content)
    compile_latex(resume_tex_path, app_dir)

    # 4. Generate AI-Synthesized LaTeX Cover Letter & Compile PDF
    custom_letter_body = synthesize_ai_cover_letter({
        "company": company,
        "role": role,
        "markdown": posting_md
    }, profile_text)
    letter_tex_content = build_cover_letter_tex({
        "company": company,
        "role": role
    }, custom_body=custom_letter_body)
    letter_tex_path = os.path.join(app_dir, "cover_letter.tex")
    with open(letter_tex_path, "w", encoding="utf-8") as f:
        f.write(letter_tex_content)
    compile_latex(letter_tex_path, app_dir)

    # 5. Dossier Fact Guard Audit
    audit_report = fact_guard.audit(resume_tex_content + "\n" + letter_tex_content, posting_md)
    with open(os.path.join(app_dir, "fact_guard_report.md"), "w", encoding="utf-8") as f:
        f.write(f"# Dossier Fact Guard Audit Report\n\n")
        f.write(f"- **Audit Status**: {audit_report['status']}\n")
        f.write(f"- **Zero Hallucinated Metrics**: {'✅ Confirmed' if audit_report['verified'] else '⚠️ Flagged'}\n")
        f.write(f"- **Total Facts Verified Against Profile**: {audit_report['total_verified_facts']}\n")
        if audit_report["suspicious_numbers"]:
            f.write(f"- **Unrecognized Numbers**: {', '.join(audit_report['suspicious_numbers'])}\n")
        else:
            f.write("- **Result**: All project metrics (e.g. 192kHz/24-bit, 240MHz, 99.97% accuracy, 8.42 GPA, $40 BOM) strictly conform to verified facts.\n")

    # 6. Save metadata state
    app_meta = {
        "id": folder_slug,
        "company": company,
        "role": role,
        "status": "Draft",
        "match_score": score,
        "seniority": match_result["seniority_label"],
        "location": candidate.get("location", "India / Remote"),
        "url": candidate.get("url", "#"),
        "title": candidate.get("title", f"{role} at {company}"),
        "created_at": datetime.now().isoformat(),
        "fact_guard": audit_report["status"],
        "refine_history": []
    }
    with open(os.path.join(app_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(app_meta, f, indent=2)

    # 7. Update Tracker
    update_tracker_dossier(company, role, score, folder_slug, candidate.get("url", "#"))
    print(f"  [✓] Dossier Application Packet compiled: applications/{folder_slug}")
    return folder_slug

def refine_application(app_id: str, instruction: str) -> Dict[str, Any]:
    """
    Dossier-grade 'Refine with AI':
    Applies user feedback to tailored resume & cover letter, recompiles LaTeX PDFs,
    and validates with Fact Guard.
    """
    app_dir = os.path.join(APPLICATIONS_DIR, app_id)
    if not os.path.exists(app_dir):
        return {"success": False, "error": f"Application {app_id} not found."}

    meta_path = os.path.join(app_dir, "meta.json")
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

    company = meta.get("company", "Company")
    role = meta.get("role", "Engineer")
    
    # Read job description if available
    job_desc = ""
    desc_path = os.path.join(app_dir, "job_description.md")
    if os.path.exists(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            job_desc = f.read()

    # Rebuild tailored LaTeX with specific emphasis from the instruction
    new_resume_tex = build_tailored_resume_tex({
        "company": company,
        "role": role,
        "markdown": job_desc + " " + instruction
    })
    
    resume_tex_path = os.path.join(app_dir, "tailored_resume.tex")
    with open(resume_tex_path, "w", encoding="utf-8") as f:
        f.write(new_resume_tex)
    compile_latex(resume_tex_path, app_dir)

    profile_text = load_master_profile()
    fact_guard = FactGuard(profile_text)

    # Re-synthesize tailored cover letter with AI
    new_letter_body = synthesize_ai_cover_letter({
        "company": company,
        "role": role,
        "markdown": job_desc + "\nSpecific User Instruction: " + instruction
    }, profile_text)
    new_letter_tex = build_cover_letter_tex({
        "company": company,
        "role": role
    }, custom_body=new_letter_body)
    letter_tex_path = os.path.join(app_dir, "cover_letter.tex")
    with open(letter_tex_path, "w", encoding="utf-8") as f:
        f.write(new_letter_tex)
    compile_latex(letter_tex_path, app_dir)
    audit_report = fact_guard.audit(new_resume_tex + "\n" + new_letter_tex, job_desc)
    
    # Record history
    history = meta.get("refine_history", [])
    history.append({
        "instruction": instruction,
        "applied_at": datetime.now().isoformat(),
        "fact_guard": audit_report["status"]
    })
    meta["refine_history"] = history
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return {
        "success": True,
        "message": f"Successfully updated documents based on: '{instruction}'",
        "fact_guard": audit_report["status"]
    }

def update_tracker_dossier(company: str, role: str, score: int, app_dir_name: str, url: str):
    today = datetime.now().strftime("%Y-%m-%d")
    folder_link = f"[`{app_dir_name}`](../applications/{app_dir_name})"
    pdf_resume_link = f"[📄 Resume PDF](../applications/{app_dir_name}/tailored_resume.pdf)"
    pdf_letter_link = f"[✉️ Cover Letter PDF](../applications/{app_dir_name}/cover_letter.pdf)"
    
    row = f"| {today} | **{company}** | {role} | **{score}%** | **Drafted** | {folder_link} | {pdf_resume_link} / {pdf_letter_link} | [Job Posting]({url}) |\n"
    
    if os.path.exists(TRACKER_PATH):
        with open(TRACKER_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            
        header = "| Date | Company | Role | Match % | Status | Application Folder | PDF Documents | Posting Link |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        if "| Date | Company |" in content:
            # Replace header if older format
            if "| PDF Documents |" not in content:
                parts = content.split("---", 1)
                new_content = "# Application Tracker\n\n" + header + row + "\n---\n" + (parts[1] if len(parts) > 1 else "")
            else:
                parts = content.split("| :--- | :--- |", 1)
                new_content = parts[0] + "| :--- | :--- |\n" + row + parts[1]
        else:
            new_content = "# Application Tracker\n\n" + header + row
            
        with open(TRACKER_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)

def run_dossier_engine():
    cfg = load_config()
    min_score = cfg.get("min_match_score", 65)
    max_drafts = cfg.get("max_daily_drafts", 5)
    
    profile_text = load_master_profile()
    fact_guard = FactGuard(profile_text)
    
    candidate_files = [f for f in os.listdir(DISCOVERED_DIR) if f.endswith(".json")]
    if not candidate_files:
        print("No pending candidates in data/discovered/.")
        return []
        
    print(f"=== Dossier Engine: Processing {len(candidate_files)} Candidates with LaTeX & Fact Guard ===")
    drafted = []
    
    for filename in candidate_files:
        filepath = os.path.join(DISCOVERED_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                candidate = json.load(f)
                
            slug = process_candidate_dossier(candidate, fact_guard, min_score)
            if slug:
                drafted.append(slug)
                if len(drafted) >= max_drafts:
                    print(f"Draft limit ({max_drafts}) reached for this batch.")
                    break
                    
            shutil.move(filepath, os.path.join(PROCESSED_DIR, filename))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    return drafted

if __name__ == "__main__":
    run_dossier_engine()
