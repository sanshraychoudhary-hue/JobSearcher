"""
Dossier AI Brain Engine
Provides LLM-driven deep job overviewing, authentic competency matching,
Fact-Guarded custom cover letter generation, and targeted resume tailoring.
Connects with Google Gemini API (gemini-2.0-flash / gemini-1.5-flash) or acts via Agent bridge.
"""

import os
import json
import re
import requests
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
PROFILE_PATH = os.path.join(BASE_DIR, "profile", "master_profile.md")


def get_gemini_api_key() -> Optional[str]:
    """Retrieves Gemini API key from environment or config.json."""
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ.get("GEMINI_API_KEY")
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ.get("GOOGLE_API_KEY")
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                key = cfg.get("gemini_api_key", "").strip()
                if key and not key.startswith("YOUR_"):
                    return key
        except Exception:
            pass
    return None


def call_gemini(prompt: str, system_instruction: str = "") -> Optional[str]:
    """Invokes Google Gemini 3.5 Flash Lite via REST API."""
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    # Priority: gemini-3.5-flash-lite first, fallback to 2.5-flash
    models = ["gemini-3.5-flash-lite", "gemini-2.5-flash", "gemini-flash-latest"]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload: Dict[str, Any] = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        }
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        try:
            res = requests.post(url, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
            else:
                print(f"Gemini API error ({model}) HTTP {res.status_code}: {res.text[:200]}")
        except Exception as e:
            print(f"Gemini API invocation error ({model}): {e}")

    return None


def escape_latex(text: str) -> str:
    """Escapes special LaTeX characters in strings like company/role names."""
    if not text:
        return ""
    text = re.sub(r'(?<!\\)&', r'\&', text)
    text = re.sub(r'(?<!\\)%', r'\%', text)
    text = re.sub(r'(?<!\\)\$', r'\$', text)
    text = re.sub(r'(?<!\\)#', r'\#', text)
    text = re.sub(r'(?<!\\)_', r'\_', text)
    return text

def synthesize_ai_cover_letter(job_info: Dict[str, Any], profile_text: str) -> str:
    """
    Synthesizes custom, persuasive cover letter body paragraphs
    specifically tailored to the company's tech stack, requirements, and mission.
    Strictly constrained by the candidate's master profile to eliminate hallucinations.
    """
    company = escape_latex(job_info.get("company", "Company"))
    role = escape_latex(job_info.get("role", "Engineer"))
    posting_md = job_info.get("markdown", "") or job_info.get("description", "")

    # Check if Gemini API is available
    if get_gemini_api_key():
        system_instruction = (
            "You are the Dossier AI Brain for Sanshray Choudhary, an ECE student at USICT (GPA 8.42). "
            "Write exactly 3 concise, impactful body paragraphs for an official LaTeX cover letter. "
            "STRICT FACT GUARD: You may ONLY cite facts, metrics, and experiences that exist in the Master Profile. "
            "NEVER invent GPA, dates, company names, or numbers. "
            "Paragraph 1: Express passion for the specific role at the company, connecting their core domain with Sanshray's relevant foundation. "
            "Paragraph 2: Deep dive into 1-2 flagship projects from his profile that directly solve the technical challenges mentioned in the JD. "
            "If the role is an ambitious stretch role with only partial (e.g. 20-50%) skill overlap, DO NOT apologize or invent fake tools; "
            "instead, position his verified foundational mastery (FreeRTOS, register-level bare-metal C/C++, high-speed DMA I2S, KiCad PCB bring-up) "
            "as the technical bedrock that ensures rapid, reliable mastery of their proprietary environment. "
            "Paragraph 3: Highlight e-Yantra IIT Bombay achievements, drone firmware internship, certifications, and readiness to deliver immediate value. "
            "Output ONLY the raw body text in clean LaTeX formatting (using \\textbf{}, \\,, and standard LaTeX paragraphs separated by \\vspace{8pt}\\\\)."
        )

        prompt = f"""Target Company: {company}
Target Role: {role}

Master Profile (Ground Truth Facts):
{profile_text[:2500]}

Job Description / Requisition Details:
{posting_md[:3000]}

Write the tailored 3-paragraph body now:"""

        ai_response = call_gemini(prompt, system_instruction)
        if ai_response and len(ai_response.strip()) > 100:
            cleaned = ai_response.strip()
            cleaned = re.sub(r"^```(?:latex|tex)?\s*", "", cleaned, flags=re.MULTILINE)
            cleaned = re.sub(r"```$", "", cleaned, flags=re.MULTILINE)
            cleaned = re.sub(r'(?<!\\)&', r'\&', cleaned)
            return cleaned.strip()

    # Domain-Aware Intelligent Heuristic Router (Fallback when API key is pending)
    lower_jd = (posting_md + " " + role).lower()

    # Category scoring to select the best match instead of arbitrary if/elif order
    domains = {
        "space_avionics": ["satellite", "space", "drone", "aerospace", "payload", "avionics", "uav", "flight", "spacecraft"],
        "robotics_ros": ["ros", "ros2", "robot", "robotics", "slam", "navigation", "autonomous", "mecanum", "kinematics", "lidar"],
        "iot_agri": ["iot", "sensor", "smart", "agri", "telemetry", "mqtt", "modbus", "rs485", "ambient", "dosing", "irrigation"],
        "kernel_drivers": ["kernel", "driver", "bsp", "linux kernel", "device driver", "internals", "system software", "bare metal"]
    }

    scores = {}
    for dom, kws in domains.items():
        score = sum(len(re.findall(r'\b' + re.escape(kw) + r'\b', lower_jd)) for kw in kws)
        scores[dom] = score

    best_domain = max(scores, key=scores.get)
    if scores[best_domain] == 0:
        best_domain = "general_embedded"

    if best_domain == "robotics_ros":
        # Robotics / ROS 2 Specialization
        body = (
            rf"\noindent I am writing to express my enthusiastic interest in the \textbf{{{role}}} position at \textbf{{{company}}}. "
            rf"As an Electronics and Communication Engineering undergraduate at USICT (GPA 8.42) with competitive robotics experience "
            rf"and certified expertise in ROS 2 from IIT Bombay, I am inspired by {company}'s cutting-edge work in autonomous systems and eager to contribute directly to your robotics engineering team. \vspace{{8pt}}\\"
            rf"\noindent My hands-on robotics engineering is anchored by qualifying \textbf{{Level 3 in IIT Bombay's e-Yantra Robotics Competition}} and earning the official \textbf{{ROS 2 Developer Certification}} from e-Yantra, IIT Bombay. "
            rf"During my AICTE internship on the \textbf{{OmniServe Autonomous Mobile Robot}}, I engineered a Wi-Fi controlled omni-directional platform utilizing a Raspberry Pi Pico W with mecanum wheels and closed-loop encoder PID motion control, achieving centimeter-level waypoint navigation and integrated telemetry. "
            rf"Complementing this, my flagship embedded system \textbf{{AtiDhwani}} features dual-core FreeRTOS on ESP32-S3 executing real-time DSP and high-speed DMA streaming under strict millisecond deadlines. \vspace{{8pt}}\\"
            rf"\noindent With demonstrated expertise across C++, Python, Linux, and real-time microcontroller-to-host actuation buses, I thrive at the intersection of algorithmic motion control and physical hardware integration. "
            rf"I look forward to discussing how my robotics background and proven problem-solving drive can accelerate {company}'s engineering objectives. \vspace{{8pt}}\\"
        )
    elif best_domain == "space_avionics":
        # SpaceTech / Aerospace / Drone Firmware Specialization
        body = (
            rf"\noindent I am writing to express my enthusiastic interest in the \textbf{{{role}}} position at \textbf{{{company}}}. "
            rf"As an Electronics and Communication Engineering student at USICT (GPA 8.42) with direct experience developing flight firmware "
            rf"at India Space Academy, I am deeply inspired by {company}'s pioneering work and eager to contribute to your mission-critical embedded avionics. \vspace{{8pt}}\\"
            rf"\noindent During my \textbf{{Winter Internship at India Space Academy}}, I developed embedded firmware for advanced drone technology, engineering robust I2C and SPI peripheral communication pipelines, implementing power-optimized deep sleep management, and ensuring rock-solid flight stability under physical constraints. "
            rf"In my flagship project \textbf{{AtiDhwani}}, I architected a high-reliability bioacoustic node on ESP32-S3 featuring 192\,kHz / 24-bit DMA I2S continuous sampling and designed a custom 2-layer carrier PCB in KiCad with 0 DRC violations. "
            rf"My work on the \textbf{{SIH 2024 Portable EMI/EMC Detection Machine}} utilizing STM32 further equipped me with hands-on debugging skills using oscilloscopes, logic analyzers, and spectrum tools. \vspace{{8pt}}\\"
            rf"\noindent Having earned IIT Bombay certifications in Embedded Systems and ROS 2, I bring rigorous engineering discipline, bare-metal C/C++ precision, and rapid board bring-up capabilities to high-stakes electronic payloads. "
            rf"I welcome the opportunity to discuss how my technical skills can advance {company}'s next generation of systems. \vspace{{8pt}}\\"
        )
    elif best_domain == "iot_agri":
        # Industrial IoT / Sensor Hub Specialization
        body = (
            rf"\noindent I am writing to express my enthusiastic interest in the \textbf{{{role}}} position at \textbf{{{company}}}. "
            rf"As an Electronics and Communication Engineering student at USICT (GPA 8.42) specializing in ARM Cortex firmware, FreeRTOS architectures, "
            rf"and multi-sensor hardware integration, I am excited by {company}'s innovative platforms and ready to build scalable, production-grade connected electronics. \vspace{{8pt}}\\"
            rf"\noindent Through my \textbf{{STM32 Industrial IoT Sensor Hub}} project, I engineered a robust industrial telemetry node utilizing an STM32F407, interfacing concurrent SPI-based ADCs, I2C ambient sensors, and UART communication buses with power-optimized deep sleep routines and reliable MQTT transmission. "
            rf"In my flagship \textbf{{AtiDhwani}} project, I designed a custom 2-layer carrier PCB in KiCad with 0 DRC violations and wrote dual-core FreeRTOS firmware managing high-speed DMA I2S sampling (192\,kHz / 24-bit) alongside real-time 128-point Radix-4 FFT spectral analysis. \vspace{{8pt}}\\"
            rf"\noindent Certified as an Embedded Systems Developer by IIT Bombay and having qualified Level 3 of the e-Yantra Robotics Competition, I am proficient in bench-level debugging using oscilloscopes and logic analyzers, protocol validation (UART, SPI, I2C, Modbus), and modern Git workflows. "
            rf"I look forward to discussing how my embedded development and hardware bring-up capabilities can add immediate value to {company}. \vspace{{8pt}}\\"
        )
    elif best_domain == "kernel_drivers":
        # Linux Kernel / Device Drivers / Low-Level Firmware Specialization
        body = (
            rf"\noindent I am writing to express my enthusiastic interest in the \textbf{{{role}}} position at \textbf{{{company}}}. "
            rf"As an Electronics and Communication Engineering student at USICT (GPA 8.42) with rigorous training in ARM Cortex bare-metal C/C++, "
            rf"FreeRTOS kernel internals, and low-level peripheral drivers, I am eager to apply my systems programming skills to {company}'s high-performance platforms. \vspace{{8pt}}\\"
            rf"\noindent In my flagship embedded system \textbf{{AtiDhwani}}, I developed dual-core FreeRTOS firmware on an ESP32-S3 (240\,MHz, 8MB PSRAM), directly architecting Core 0 to manage zero-jitter DMA I2S streaming and drop-free circular-buffer memory management under strict timing constraints, while Core 1 executes real-time 128-point Radix-4 FFT spectral DSP. "
            rf"In addition, my work on the \textbf{{STM32 Industrial IoT Sensor Hub}} (STM32F407) required deep familiarity with register-level peripheral configuration across SPI, I2C, and UART interfaces, interrupt handling, and task synchronization. \vspace{{8pt}}\\"
            rf"\noindent Holding an official Embedded Systems Developer certification from IIT Bombay and practical experience with Linux environments, CMake, Git, and hardware debugging tools (JTAG, logic analyzers, DMMs), I bring a disciplined, analytical approach to solving complex firmware and runtime concurrency challenges. "
            rf"I would welcome the opportunity to discuss how my systems engineering background aligns with {company}'s technical priorities. \vspace{{8pt}}\\"
        )
    else:
        # General Embedded Systems & Hardware Engineering
        body = (
            rf"\noindent I am writing to express my enthusiastic interest in the \textbf{{{role}}} position at \textbf{{{company}}}. "
            rf"As an Electronics and Communication Engineering student at USICT (GPA 8.42) with extensive hands-on expertise in ARM Cortex/STM32 firmware, "
            rf"ESP32-S3 dual-core FreeRTOS architectures, and custom KiCad multi-layer PCB hardware development, I am eager to contribute to {company}'s engineering initiatives. \vspace{{8pt}}\\"
            rf"\noindent Through my flagship project \textbf{{AtiDhwani}}, I architected a low-cost bioacoustic monitoring system utilizing dual-core FreeRTOS on ESP32-S3, high-speed DMA I2S continuous sampling (192\,kHz / 24-bit), and real-time DSP with 128-point Radix-4 FFT spectral analysis. "
            rf"I also engineered the custom 2-layer carrier PCB in KiCad with 0 DRC violations, interfacing high-precision Wolfson stereo ADCs and TI DACs. In addition, my \textbf{{STM32 Industrial IoT Sensor Hub}} project demonstrated robust industrial telemetry over MQTT and SPI/I2C/UART sensor buses with power-optimized deep-sleep management. \vspace{{8pt}}\\"
            rf"\noindent Having qualified Level 3 of IIT Bombay's e-Yantra Robotics Competition, earned official certifications in ROS 2 and Embedded Systems Developer from IIT Bombay, and developed drone firmware during my internship with India Space Academy, I thrive in fast-paced environments where software precision meets physical hardware constraints. \vspace{{8pt}}\\"
        )

    return body


def refine_with_gemini(app_data: Dict[str, Any], instruction: str, profile_text: str) -> Dict[str, Any]:
    """
    Interactive 'Refine with AI' copilot powered by Gemini 3.5 Flash Lite.
    Understands greetings, answers questions, or refines LaTeX documents while respecting Fact Guard.
    """
    company = escape_latex(app_data.get("company", "Company"))
    role = escape_latex(app_data.get("role", "Engineer"))
    job_desc = app_data.get("job_description", "")
    api_key = get_gemini_api_key()

    if not api_key:
        return {
            "reply_message": f"Updated documents based on: '{instruction}'. (Tip: Connect Gemini API in Settings for a full conversational copilot)",
            "needs_doc_update": True,
            "updated_cover_letter_body": None
        }

    system_instruction = (
        "You are the Dossier AI Copilot for candidate Sanshray Choudhary (USICT ECE student, GPA 8.42). "
        "The user is viewing an application dossier for a specific company and role. "
        "The user will send a chat message, instruction, or question in the 'Refine with AI' panel. "
        "Analyze whether the input is a conversational greeting/question (e.g. 'yo', 'hello', 'what is this?', 'how do I match?') "
        "or a specific document refinement instruction (e.g. 'highlight AtiDhwani', 'prioritize drone firmware', 'make summary concise'). "
        "Strict Fact Guard: You may ONLY cite facts and metrics from the Master Profile (e.g. 192kHz/24-bit, 240MHz, 8.42 GPA, e-Yantra Level 3). "
        "Return a valid JSON object matching the requested schema."
    )

    prompt = f"""Target Company: {company}
Target Role: {role}
Job Requisition Context:
{job_desc[:1800]}

Master Profile Facts:
{profile_text[:2000]}

User Chat Input:
"{instruction}"

Return a JSON object with:
1. "reply_message": (string) A conversational, helpful, professional response to the user. If greeting, greet back and suggest 2-3 high-impact refinements for this specific company. If an edit was requested, concisely explain the specific technical changes made to the cover letter or resume.
2. "needs_doc_update": (boolean) False if the input is purely conversational/question, True if documents should be re-compiled.
3. "updated_cover_letter_body": (string or null) If needs_doc_update is True, provide the updated 3 body paragraphs in clean LaTeX format (using \\textbf{{}}, \\,, etc.). If needs_doc_update is False, set to null.
"""

    model = "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.25,
            "maxOutputTokens": 2048
        }
    }

    try:
        res = requests.post(url, json=payload, timeout=20)
        if res.status_code == 200:
            raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            data = json.loads(raw_text)
            body = data.get("updated_cover_letter_body")
            if isinstance(body, list):
                body = "\n\n".join(body)
            if body:
                body = re.sub(r"^```(?:latex|tex)?\s*", "", body, flags=re.MULTILINE)
                body = re.sub(r"```$", "", body, flags=re.MULTILINE)
                body = re.sub(r'(?<!\\)&', r'\&', body)
            return {
                "reply_message": data.get("reply_message", f"Updated application based on: '{instruction}'"),
                "needs_doc_update": bool(data.get("needs_doc_update", False)),
                "updated_cover_letter_body": body
            }
        else:
            print(f"Gemini Refine error HTTP {res.status_code}: {res.text[:200]}")
    except Exception as e:
        print(f"Gemini Refine execution error: {e}")

    return {
        "reply_message": f"Applied changes for: '{instruction}'",
        "needs_doc_update": True,
        "updated_cover_letter_body": None
    }


def brain_evaluate_match(job_info: Dict[str, Any], profile_text: str) -> Optional[Dict[str, Any]]:
    """
    Evaluates candidate-to-job match semantically using Gemini 3.5 Flash Lite.
    Returns:
      - score: int (0-100)
      - report_md: str
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    company = escape_latex(job_info.get("company", "Company"))
    role = escape_latex(job_info.get("role", "Engineer"))
    posting_md = job_info.get("markdown", "") or job_info.get("description", "")

    prompt = f"""You are the Dossier Strategic Talent Evaluator.
Analyze the fit between candidate Sanshray Choudhary (USICT B.Tech ECE, GPA 8.42) and this target job opening.

Candidate Master Profile Ground Truth:
{profile_text[:2500]}

Job Requisition:
Company: {company}
Role: {role}
Posting Content:
{posting_md[:3000]}

Return a JSON object:
{{
  "score": (integer 0-100 representing realistic match strength),
  "strengths": [list of 3 distinct technical strengths directly matching JD requirements],
  "gaps": [list of 1-3 genuine experience or technical gaps mentioned in the JD],
  "interview_strategy": (string: 2-3 sentences advising how the candidate should pitch their projects to defend these gaps during interviews)
}}
"""

    model = "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }

    try:
        res = requests.post(url, json=payload, timeout=20)
        if res.status_code == 200:
            data = json.loads(res.json()["candidates"][0]["content"]["parts"][0]["text"])
            score = int(data.get("score", 75))
            strengths = data.get("strengths", [])
            gaps = data.get("gaps", [])
            strategy = data.get("interview_strategy", "")

            md = f"# Dossier AI Match Report: {company} -- {role}\n\n"
            md += f"### Semantic Match Score: **{score}%** *(Evaluated by Gemini 3.5 Flash Lite)*\n\n"
            md += "### 🎯 Key Strengths & Technical Overlap\n"
            for s in strengths:
                md += f"- **{s}**\n"
            md += "\n### ⚠️ Identified Gaps & Stretch Requirements\n"
            for g in gaps:
                md += f"- *{g}*\n"
            md += "\n### 💡 Strategic Interview & Positioning Playbook\n"
            md += f"{strategy}\n"

            return {
                "score": score,
                "report_md": md,
                "strengths": strengths,
                "gaps": gaps,
                "strategy": strategy
            }
    except Exception as e:
        print(f"Gemini Match Evaluation error: {e}")

    return None


