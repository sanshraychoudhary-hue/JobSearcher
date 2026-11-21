"""
Matcher and Application Drafter Module
Evaluates candidate job postings against master_profile.md and drafts tailored applications.
"""

import json
import os
import re
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "profile", "master_profile.md")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DISCOVERED_DIR = os.path.join(BASE_DIR, "data", "discovered")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
APPLICATIONS_DIR = os.path.join(BASE_DIR, "applications")
TRACKER_PATH = os.path.join(BASE_DIR, "tracker", "tracker.md")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(APPLICATIONS_DIR, exist_ok=True)

COMMON_SKILLS = [
    "c", "c++", "embedded", "firmware", "rtos", "freertos", "stm32", "esp32", "arm cortex",
    "kicad", "pcb design", "i2c", "spi", "i2s", "uart", "can", "can bus", "rs-485", "modbus",
    "mqtt", "iot", "robotics", "ros", "ros2", "dsp", "signal processing", "tinyml", "tensorflow",
    "tflite", "opencv", "dma", "adc", "dac", "fpga", "vhdl", "verilog", "iec 61508", "functional safety",
    "pid", "control systems", "sensors", "actuators", "oscilloscope", "logic analyzer", "hardware debugging",
    "python", "matlab", "git", "linux", "stm32cube", "iar", "arduino", "docker"
]

def load_master_profile() -> str:
    if not os.path.exists(PROFILE_PATH):
        raise FileNotFoundError(f"Missing master profile at {PROFILE_PATH}")
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_profile_details(profile_text: str):
    """Parses basic fields from master_profile.md"""
    name_match = re.search(r"\*\*Full Name\*\*:\s*(.+)", profile_text)
    email_match = re.search(r"\*\*Email\*\*:\s*(.+)", profile_text)
    phone_match = re.search(r"\*\*Phone\*\*:\s*(.+)", profile_text)
    linkedin_match = re.search(r"\*\*LinkedIn\*\*:\s*(.+)", profile_text)
    github_match = re.search(r"\*\*GitHub\*\*:\s*(.+)", profile_text)
    location_match = re.search(r"\*\*Location\*\*:\s*(.+)", profile_text)
    
    return {
        "name": name_match.group(1).strip() if name_match else "Candidate",
        "email": email_match.group(1).strip() if email_match else "email@example.com",
        "phone": phone_match.group(1).strip() if phone_match else "",
        "linkedin": linkedin_match.group(1).strip() if linkedin_match else "",
        "github": github_match.group(1).strip() if github_match else "",
        "location": location_match.group(1).strip() if location_match else "",
    }

def analyze_match(posting_text: str, profile_text: str):
    """Calculates skill overlap, match score, and missing keywords."""
    posting_lower = posting_text.lower()
    profile_lower = profile_text.lower()
    
    required_keywords = []
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', posting_lower):
            required_keywords.append(skill)
            
    if not required_keywords:
        # Fallback keywords if none detected
        required_keywords = ["python", "c++", "linux", "git", "rest", "sql"]
        
    matched = [k for k in required_keywords if k in profile_lower]
    missing = [k for k in required_keywords if k not in profile_lower]
    
    score = int((len(matched) / len(required_keywords)) * 100) if required_keywords else 80
    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "total_required": len(required_keywords)
    }

def update_tracker(company: str, role: str, score: int, app_dir_name: str, url: str):
    today = datetime.now().strftime("%Y-%m-%d")
    folder_link = f"[`{app_dir_name}`](../applications/{app_dir_name})"
    row = f"| {today} | {company} | {role} | **{score}%** | **Drafted** | {folder_link} | [View Posting]({url}) |\n"
    
    if os.path.exists(TRACKER_PATH):
        with open(TRACKER_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Append before the separator or at the end of the table
        if "| :--- | :--- |" in content:
            parts = content.split("| :--- | :--- |\n", 1)
            new_content = parts[0] + "| :--- | :--- |\n" + row + parts[1]
        else:
            new_content = content + "\n" + row
            
        with open(TRACKER_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)

def draft_application(candidate: dict, profile_text: str, profile_info: dict, match_res: dict):
    company = candidate["company"]
    role = candidate["role"]
    score = match_res["score"]
    matched_skills = ", ".join(match_res["matched"]).title()
    missing_skills = ", ".join(match_res["missing"]).title() if match_res["missing"] else "None identified"
    
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
        f.write(f"- **Original URL**: {candidate.get('url', '#')}\n")
        f.write(f"- **Discovered At**: {candidate.get('discovered_at', '')}\n\n")
        f.write("## Posting Details\n\n")
        f.write(candidate.get("markdown", "No content captured."))
        
    # 2. Match Analysis
    with open(os.path.join(app_dir, "match_analysis.md"), "w", encoding="utf-8") as f:
        f.write(f"# Match Analysis: {company} – {role}\n\n")
        f.write(f"### Overall Match Score: **{score}%**\n\n")
        f.write("### Matched Competencies\n")
        f.write(f"The profile satisfies these posting requirements: **{matched_skills}**\n\n")
        f.write("### Potential Skill Gaps\n")
        f.write(f"Items mentioned in posting not explicitly detailed in profile: **{missing_skills}**\n\n")
        f.write("### Recommendation\n")
        if score >= 75:
            f.write("✅ **High match.** Strong candidate for application. Highlight project telemetry and architecture experience in interview.\n")
        else:
            f.write("⚠️ **Moderate match.** Verify if transferable skills can address the missing requirements.\n")

    # 3. Tailored Resume (ATS-friendly)
    with open(os.path.join(app_dir, "tailored_resume.md"), "w", encoding="utf-8") as f:
        f.write(f"# {profile_info['name']}\n\n")
        f.write(f"Email: [{profile_info['email']}](mailto:{profile_info['email']}) | Phone: {profile_info['phone']} | Location: {profile_info['location']}\n\n")
        f.write(f"[LinkedIn Profile]({profile_info['linkedin']}) | [GitHub Profile]({profile_info['github']})\n\n")
        f.write(f"## Target Position: {role} — {company}\n\n")
        f.write("### Professional Summary\n")
        f.write(f"Electronics & Communication Engineering professional and Embedded Systems Developer with hands-on expertise in **{matched_skills}**. Proven track record designing high-speed KiCad multi-layer PCBs, dual-core FreeRTOS firmware (ESP32-S3 / STM32), real-time DSP, industrial IoT architectures, and ROS 2 robotics. Certified by e-Yantra (IIT Bombay) in Embedded Systems & ROS 2. Focused on applying robust hardware-software co-design and reliability engineering to {company}'s products.\n\n")
        f.write("### Core Technical Competencies\n")
        f.write(f"- **Matching Technologies**: {matched_skills}\n")
        f.write("- **Hardware & Embedded**: ARM Cortex-M3/M4, STM32, ESP32-S3, FreeRTOS, KiCad PCB Design, SPI, I2C, I2S, CAN Bus, Modbus, UART, DMA, Logic Analyzers\n")
        f.write("- **Software & AI**: C, C++, Python, MATLAB, TinyML, TensorFlow Lite, OpenCV, ROS/ROS 2, Git, Linux\n\n")
        f.write("### Relevant Engineering Experience\n")
        f.write("#### Winter Intern — India Space Academy (Feb 2026 – Mar 2026)\n")
        f.write("- Developed embedded firmware for advanced drone technology utilizing microcontrollers, I2C/SPI interfaces, and optimized power management.\n")
        f.write("- Implemented real-time sensor polling routines and robust fail-safes for critical flight stability.\n\n")
        f.write("#### Project Intern — AICTE (Jun 2025 – Aug 2025)\n")
        f.write("- Engineered OmniServe: an autonomous Wi-Fi controlled mobile robot using Raspberry Pi Pico W, mecanum wheels, and closed-loop encoder PID control.\n\n")
        f.write("### Highlighted Projects Aligned with Role\n")
        f.write("#### AtiDhwani — ESP32-S3 Bioacoustics PAM Node & Detector (Nov 2026 – Present)\n")
        f.write("- Engineered modular PAM node with dual-core FreeRTOS on ESP32-S3 (240MHz, 8MB PSRAM), DMA I2S streaming, and FAT32 WAV circular logging.\n")
        f.write("- Implemented real-time DSP with quadrature heterodyne down-conversion and 128-pt Radix-4 FFT spectral analysis displayed on OLED at 30 FPS.\n")
        f.write("- Designed custom 2-layer carrier PCB in KiCad (0 DRC) with dual MEMS mics, Wolfson 24-bit stereo ADC, and TI 32-bit DAC.\n\n")
        f.write("#### STM32 Industrial IoT Sensor Hub\n")
        f.write("- Developed industrial sensor node using STM32F407 interfacing SPI ADCs, I2C temperature, and UART gas sensors.\n")
        f.write("- Implemented FreeRTOS firmware managing concurrent sensor sampling, digital filtering, and reliable MQTT telemetry over ESP8266.\n\n")
        f.write("### Education & Credentials\n")
        f.write("- **B.Tech, Electronics and Communication Engineering** — USICT, Dwarka (2023 – 2027) | **GPA: 8.42/10**\n")
        f.write("- **Certifications (IIT Bombay e-Yantra)**: e-Yantra Robotics Level 3, ROS 2 Developer, Embedded Systems Developer\n")

    # 4. Cover Letter
    with open(os.path.join(app_dir, "cover_letter.md"), "w", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%B %d, %Y')}\n\n")
        f.write(f"Hiring Team — {company}\n\n")
        f.write(f"**Subject**: Application for {role} – Sanshray Choudhary\n\n")
        f.write(f"Dear Hiring Team at {company},\n\n")
        f.write(f"I am writing to express my strong enthusiasm for the **{role}** position at **{company}**. As an Electronics and Communication Engineering student at USICT (GPA 8.42) with rigorous hands-on experience in **{matched_skills}**, FreeRTOS, STM32/ESP32 firmware, and custom PCB hardware design, I am eager to contribute to {company}'s high-reliability engineering initiatives.\n\n")
        f.write(f"Through projects like **AtiDhwani** (an ESP32-S3 dual-core bioacoustic detector with high-speed DMA I2S, KiCad 2-layer PCB, and real-time DSP) and my **STM32 Industrial IoT Sensor Hub**, I have developed a disciplined approach to hardware-software co-design, protocol integration (CAN, SPI, I2C, Modbus, MQTT), and power-constrained optimization. Furthermore, having qualified Level 3 of IIT Bombay's e-Yantra Robotics Competition and completed drone firmware development with India Space Academy, I thrive in tackling challenging embedded systems and automation problems.\n\n")
        f.write(f"{company}'s reputation for engineering excellence and industrial innovation makes this role an ideal match for my technical skills and ambitions. I would welcome the opportunity to discuss how my firmware, hardware, and systems expertise can bring immediate value to your team.\n\n")
        f.write(f"Thank you for your time and consideration.\n\n")
        f.write(f"Sincerely,\n\n**Sanshray Choudhary**\n{profile_info['email']} | {profile_info['phone']}\nLinkedIn: {profile_info['linkedin']}\nGitHub: {profile_info['github']}\n")

    # 5. Update Tracker
    update_tracker(company, role, score, folder_slug, candidate.get("url", "#"))
    print(f"  [✓] Application packet created: applications/{folder_slug} (Match: {score}%)")
    return folder_slug

def process_discovered_candidates():
    cfg = load_config()
    min_score = cfg.get("min_match_score", 70)
    max_drafts = cfg.get("max_daily_drafts", 5)
    
    profile_text = load_master_profile()
    profile_info = extract_profile_details(profile_text)
    
    candidate_files = [f for f in os.listdir(DISCOVERED_DIR) if f.endswith(".json")]
    if not candidate_files:
        print("No new candidate files found in data/discovered/.")
        return []
    
    print(f"=== Evaluating {len(candidate_files)} Candidate Postings ===")
    drafted_count = 0
    drafted_apps = []
    
    for filename in candidate_files:
        filepath = os.path.join(DISCOVERED_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                candidate = json.load(f)
                
            match_res = analyze_match(candidate.get("markdown", "") + " " + candidate.get("title", ""), profile_text)
            score = match_res["score"]
            print(f"Evaluating: {candidate['company']} - {candidate['title']} -> Score: {score}%")
            
            if score >= min_score and drafted_count < max_drafts:
                slug = draft_application(candidate, profile_text, profile_info, match_res)
                drafted_apps.append(slug)
                drafted_count += 1
            else:
                print(f"  [-] Skipped drafting (Score {score}% below threshold {min_score}% or draft limit reached).")
                
            # Move to processed
            shutil.move(filepath, os.path.join(PROCESSED_DIR, filename))
            
        except Exception as e:
            print(f"  [!] Error processing {filename}: {e}")
            
    print(f"\nProcessing complete! Drafted {drafted_count} new applications.")
    return drafted_apps

if __name__ == "__main__":
    process_discovered_candidates()
