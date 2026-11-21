"""
Dossier-Grade LaTeX & PDF Generation Engine
Dynamically tailors Sanshray Choudhary's exact LaTeX CV and Cover Letter,
prioritizes the most relevant projects based on job requirements,
and compiles them to high-resolution PDFs via pdflatex.
"""

import os
import re
import subprocess
from datetime import datetime
from typing import Dict, List, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MY_CV_DIR = os.path.join(BASE_DIR, "my CV")
CV_TEX_PATH = os.path.join(MY_CV_DIR, "Sanshray_Choudhary_Updated_CV.tex")

# Modular project definitions from Sanshray's CV with their keyword triggers
PROJECTS_DATABASE = [
    {
        "id": "atidhwani",
        "title": "AtiDhwani -- ESP32-S3 Ultrasonic Bat PAM Node & Bioacoustics Detector",
        "date": "Nov 2026 -- Present",
        "tags": ["embedded", "firmware", "esp32", "freertos", "kicad", "pcb", "dsp", "i2s", "dma", "adc", "dac", "c", "c++", "signal processing"],
        "latex": r"""\noindent \textbf{AtiDhwani -- ESP32-S3 Ultrasonic Bat PAM Node \& Bioacoustics Detector} \hfill Nov 2026 -- Present%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Engineered an open-source modular Passive Acoustic Monitoring (PAM) node and handheld bat detector capturing 10--96\,kHz wildlife bioacoustics with 192\,kHz / 24-bit continuous sampling at $<$ \$40 BOM cost (vs.\ \$1,000--\$3,500 commercial systems).%
\item Developed dual-core FreeRTOS firmware on ESP32-S3 (240\,MHz, 8MB Octal PSRAM): Core 0 manages high-speed DMA I2S streaming and drop-free FAT32 WAV logging to MicroSD via a 3.6MB circular PSRAM buffer.%
\item Implemented real-time DSP on Core 1 executing quadrature heterodyne down-conversion (tunable 15--90\,kHz LO), frequency division, and 128-point Radix-4 FFT spectral analysis displayed on a 0.91" SSD1306 OLED at 30\,FPS.%
\item Designed custom 2-layer carrier PCB in KiCad (0 DRC violations) integrating dual MEMS microphones, ultra-low-noise LDO, 24-bit Wolfson WM8782 stereo ADC (Master Mode, 24.576\,MHz crystal), and 32-bit TI PCM5102A DAC driving field headphones with zero perceived latency.%
\end{itemize} \vspace{8pt}"""
    },
    {
        "id": "stm32_hub",
        "title": "STM32 Industrial IoT Sensor Hub",
        "date": "Jan 2025",
        "tags": ["stm32", "industrial", "iot", "freertos", "c", "c++", "spi", "i2c", "uart", "mqtt", "sensors", "firmware", "low power", "arm cortex"],
        "latex": r"""\noindent \textbf{STM32 Industrial IoT Sensor Hub} \hfill Jan 2025%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Developed a high-performance industrial sensor node using STM32F407, interfacing with SPI-based ADCs, I2C temperature sensors, and UART gas sensors.%
\item Implemented a lightweight FreeRTOS firmware to manage concurrent sensor sampling, data filtering, and reliable MQTT transmission over an ESP8266 Wi-Fi module.%
\item Designed an intelligent power management algorithm using deep sleep modes to maximize battery life in remote deployments.%
\end{itemize} \vspace{8pt}"""
    },
    {
        "id": "aegis_guardian",
        "title": "Aegis Guardian - AI Fall Detection & Health Monitoring System",
        "date": "Oct 2025",
        "tags": ["ai", "tinyml", "tflite", "esp32", "machine learning", "sensors", "python", "wearable", "iot", "firmware"],
        "latex": r"""\noindent \textbf{Aegis Guardian - AI Fall Detection \& Health Monitoring System} \hfill Oct 2025%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Engineered an ESP32-based embedded wearable system for real-time fall detection and vital monitoring.%
\item Developed firmware for 50Hz sensor acquisition (MPU6050, AD8232, BMP180) using I2C/ADC with optimized Wi-Fi data streaming to a Python ML inference server.%
\item Implemented a multi-model pipeline (Random Forest + TFLite CNN) achieving 99.97\% accuracy with sub-50ms latency, and integrated cloud sync for remote monitoring.%
\end{itemize} \vspace{8pt}"""
    },
    {
        "id": "omniserve",
        "title": "OmniServe (Internship Project)",
        "date": "Jun 2025",
        "tags": ["robotics", "ros", "ros2", "pid", "control systems", "pico", "raspberry pi", "python", "telemetry", "actuators"],
        "latex": r"""\noindent \textbf{OmniServe (Internship Project)} \hfill Jun 2025%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Developed an autonomous Wi-Fi controlled omni-directional mobile robot using Raspberry Pi Pico W with mecanum wheels, encoder-based PID motion control, and centimeter-level navigation accuracy.%
\item Implemented a web-based control dashboard with real-time telemetry and integrated a robotic arm for basic pick-and-place operations, validated under real-world load conditions.%
\end{itemize} \vspace{8pt}"""
    },
    {
        "id": "emi_emc",
        "title": "Portable EMI/EMC detection machine - SIH 2024",
        "date": "Jun 2024",
        "tags": ["stm32", "analog", "emi", "emc", "hardware", "signal processing", "electronics", "circuit design"],
        "latex": r"""\noindent \textbf{Portable EMI/EMC detection machine - SIH 2024} \hfill Jun 2024%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Developed a portable EMI/EMC meter for metro networks using STM32F401VE, AD633, LMF380, and OLED12864, featuring onboard sensors and wireless monitoring.%
\end{itemize} \vspace{8pt}"""
    },
    {
        "id": "railway_monitoring",
        "title": "AI Acoustic Railway Monitoring - SIH 2024",
        "date": "Jun 2024",
        "tags": ["fpga", "vhdl", "verilog", "signal processing", "ai", "acoustic", "sensors", "reinforcement learning"],
        "latex": r"""\noindent \textbf{AI Acoustic Railway Monitoring - SIH 2024} \hfill Jun 2024%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Combined Station-Based Acoustic Systems (SBAS) and onboard sensors for real-time railway crack detection using autoencoders, reinforcement learning, and FPGA.%
\item Predicted cracks for preventive maintenance, improving railway safety and efficiency.%
\end{itemize} \vspace{8pt}"""
    },
    {
        "id": "smart_helmet",
        "title": "Sanchalak Kavach (Smart Helmet)",
        "date": "Jun 2024",
        "tags": ["esp32", "sensors", "bluetooth", "safety", "iot", "firmware", "wearable"],
        "latex": r"""\noindent \textbf{Sanchalak Kavach (Smart Helmet) (Internship Project)} \hfill Jun 2024%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Built a smart helmet attachment with HUD navigation, crash detection (MPU6050, BMP280), and SMS alerts via ESP32.%
\item Integrated Bluetooth for Android, built-in ventilation, vibration motors, and speakers, featuring an AI-based crash prediction model.%
\end{itemize} \vspace{8pt}"""
    },
    {
        "id": "sonicbeam",
        "title": "SonicBeam Personalised Audio",
        "date": "Jul 2025",
        "tags": ["audio", "opencv", "computer vision", "python", "rf", "embedded"],
        "latex": r"""\noindent \textbf{SonicBeam Personalised Audio} \hfill Jul 2025%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Developed an embedded assistive guidance system leveraging FM-based directional audio amplification for personalized, non-intrusive audio cues.%
\item Integrated embedded hardware with OpenCV-based computer vision in Python for real-time user detection and location awareness, targeting accessibility applications.%
\end{itemize} \vspace{8pt}"""
    },
    {
        "id": "self_balancing_bot",
        "title": "Self-Balancing Bot - eYantra 2024",
        "date": "Sep 2024",
        "tags": ["robotics", "pid", "control systems", "arduino", "simulation", "python"],
        "latex": r"""\noindent \textbf{Self-Balancing Bot - eYantra 2024 (Stage 1 – Qualified)} \hfill Sep 2024%
\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]%
\item Built a self-balancing robot using an Arduino Nano, MPU6050, and encoders. Tuned the PID controller and simulated in Python/CoppeliaSim.%
\end{itemize} \vspace{8pt}"""
    }
]

def rank_projects(job_description: str) -> List[Dict[str, Any]]:
    """Ranks projects dynamically based on keyword overlap with the job description."""
    desc_lower = job_description.lower()
    scored_projects = []
    
    for proj in PROJECTS_DATABASE:
        score = 0
        for tag in proj["tags"]:
            if re.search(r'\b' + re.escape(tag) + r'\b', desc_lower):
                score += 2
        scored_projects.append((score, proj))
        
    scored_projects.sort(key=lambda x: x[0], reverse=True)
    return [p[1] for p in scored_projects]

def build_tailored_resume_tex(job_info: Dict[str, Any]) -> str:
    """Builds a customized LaTeX resume prioritizing matching projects."""
    ranked_projects = rank_projects(job_info.get("markdown", "") + " " + job_info.get("role", ""))
    
    # Take the top 5 most relevant projects for high impact
    top_projects_latex = "\n\n".join([p["latex"] for p in ranked_projects[:5]])
    
    company = job_info.get("company", "Engineering Firm")
    role = job_info.get("role", "Embedded Systems Engineer")
    
    resume_tex = rf"""\documentclass[10pt,a4paper]{{article}}%
\usepackage[T1]{{fontenc}}%
\usepackage[utf8]{{inputenc}}%
\usepackage{{lmodern}}%
\usepackage{{textcomp}}%
\usepackage{{lastpage}}%
\usepackage{{geometry}}%
\geometry{{margin=0.65in}}%
%
\usepackage{{enumitem}}%
\usepackage{{hyperref}}%
\usepackage{{titlesec}}%
\usepackage{{xcolor}}%
\titleformat{{\section}}{{\large\bfseries\uppercase}}{{}}{{0em}}{{}}[\titlerule]%
\titlespacing{{\section}}{{0pt}}{{10pt}}{{6pt}}%
\pagestyle{{empty}}%
%
\begin{{document}}%
\normalsize%
\noindent {{\fontsize{{26}}{{32}}\selectfont \textbf{{Sanshray Choudhary}}}} \vspace{{3pt}}\\%
\noindent \textbf{{\scriptsize sanshray.choudhary@gmail.com $\bullet$ +91 9810894391 $\bullet$ \href{{https://www.linkedin.com/in/sanshray-choudhary-3591b9282}}{{https://www.linkedin.com/in/sanshray-choudhary-3591b9282}} \\ \href{{https://github.com/sanshraychoudhary-hue}}{{https://github.com/sanshraychoudhary-hue}}}} \vspace{{6pt}}%

\section*{{Target Position: {role} -- {company}}}%
\noindent \textit{{Electronics \& Communication Engineer (USICT, GPA 8.42) specializing in ARM Cortex/STM32, ESP32-S3 FreeRTOS firmware, custom KiCad PCB hardware design, and protocol integration (CAN, Modbus, I2S, SPI, I2C). e-Yantra IIT Bombay Certified in Embedded Systems \& ROS 2.}} \vspace{{6pt}}%

\section*{{Education}}%
\noindent \textbf{{University School of Information, Communication and Technology, Dwarka - 110078}} \hfill 2023--2027 \\%
\indent \textit{{Bachelor of Technology, Electronics and Communication Engineering (8.42 GPA)}} \vspace{{6pt}}\\%
\noindent \textbf{{The Air Force School, Subroto Park, Delhi Cantt - 110010}} \hfill 2009--2022 \\%
\indent \textit{{Senior Secondary (XII) (PCM), CBSE (93.8\%) $\bullet$ Secondary (X), CBSE (94.6\%)}} \vspace{{6pt}}%

\section*{{Licenses \& Certifications}}%
\noindent \textbf{{e-Yantra Robotics Competition (Level 3)}} \hfill Mar 2025 \\%
\indent \textit{{Issued by e-Yantra, IIT Bombay}} \vspace{{4pt}}\\%
\noindent \textbf{{ROS 2 Developer}} \hfill Feb 2025 \\%
\indent \textit{{Issued by e-Yantra, IIT Bombay}} \vspace{{4pt}}\\%
\noindent \textbf{{Embedded Systems Developer}} \hfill Dec 2024 \\%
\indent \textit{{Issued by e-Yantra, IIT Bombay}} \vspace{{6pt}}%

\section*{{Professional Experience}}%
\noindent \textbf{{Winter Intern, India Space Academy}} \hfill Feb 2026 -- Mar 2026%
\begin{{itemize}}[leftmargin=15pt, nosep, topsep=0pt]%
\item Developed embedded firmware for advanced drone technology utilizing microcontrollers, I2C/SPI interfaces, and optimized power management.%
\end{{itemize}} \vspace{{6pt}}%

\noindent \textbf{{Project Intern, AICTE (OmniServe Robot)}} \hfill Jun 2025 -- Aug 2025%
\begin{{itemize}}[leftmargin=15pt, nosep, topsep=0pt]%
\item Engineered an autonomous Wi-Fi mobile robot using Raspberry Pi Pico W, mecanum wheels, and closed-loop encoder PID control.%
\end{{itemize}} \vspace{{6pt}}%

\noindent \textbf{{TechSpace, Joint Secretary}} \hfill Nov 2024 -- Present%
\begin{{itemize}}[leftmargin=15pt, nosep, topsep=0pt]%
\item Facilitated technical events, workshops, and embedded systems seminars to foster peer-to-peer technical growth.%
\end{{itemize}} \vspace{{6pt}}%

\noindent \textbf{{Internship Trainee, BSNL}} \hfill Jun 2026 -- Jul 2026 \vspace{{6pt}}%

\section*{{Highlighted Relevant Projects}}%
{top_projects_latex}

\section*{{Core Technical Skills}}%
\noindent \textbf{{Core Electronics \& Embedded Systems:}} Microcontrollers (ARM Cortex M3/M4, STM32, ESP32, Arduino), IoT, Robotics, Signal Processing (FFT, Filtering), Digital Electronics, Circuit Design, PCB Design (KiCad), FreeRTOS, Sensors \& Actuators, Control Systems, PID Control, Power Electronics, CNC Machining, STM32Cube, Protocols \& Interfaces (SPI, I2C, I2S, UART, CAN, RS-485, Modbus, MQTT), Hardware Debugging (Logic Analyzers, Oscilloscopes) \vspace{{6pt}}\\%
\noindent \textbf{{Software \& Tools:}} C, C++, Python, MATLAB, TinyML, TensorFlow Lite, OpenCV, ROS/ROS 2, Git, Linux, Simulation \& Modelling (CoppeliaSim)%
\end{{document}}"""
    return resume_tex

def build_cover_letter_tex(job_info: Dict[str, Any], custom_body: Optional[str] = None) -> str:
    """Builds an elegant LaTeX cover letter with either AI-custom body or domain-tailored content."""
    company = job_info.get("company", "Company")
    role = job_info.get("role", "Engineer")
    date_str = datetime.now().strftime("%B %d, %Y")
    
    if custom_body and len(custom_body.strip()) > 50:
        body_content = custom_body
    else:
        # Default fallback
        body_content = rf"""\noindent I am writing to express my enthusiastic interest in the \textbf{{{role}}} position at \textbf{{{company}}}. As an Electronics and Communication Engineering student at USICT (GPA 8.42) with extensive hands-on expertise in ARM Cortex/STM32 firmware, ESP32-S3 dual-core FreeRTOS architectures, and custom KiCad multi-layer PCB hardware development, I am eager to contribute to {company}'s industry-leading engineering initiatives. \vspace{{8pt}}\\%
\noindent Through my flagship project \textbf{{AtiDhwani}}, I architected a low-cost bioacoustic monitoring system utilizing dual-core FreeRTOS on ESP32-S3, high-speed DMA I2S continuous sampling (192\,kHz / 24-bit), and real-time DSP with 128-point Radix-4 FFT spectral analysis. I also engineered the custom 2-layer carrier PCB in KiCad with 0 DRC violations, interfacing high-precision Wolfson stereo ADCs and TI DACs. In addition, my \textbf{{STM32 Industrial IoT Sensor Hub}} project demonstrated robust industrial telemetry over MQTT and SPI/I2C/UART sensor buses with power-optimized deep-sleep management. \vspace{{8pt}}\\%
\noindent Having qualified Level 3 of IIT Bombay's e-Yantra Robotics Competition, earned official certifications in ROS 2 and Embedded Systems Developer from IIT Bombay, and developed drone firmware during my internship with India Space Academy, I thrive in fast-paced environments where software precision meets physical hardware constraints. \vspace{{8pt}}\\%"""

    letter_tex = rf"""\documentclass[10pt,a4paper]{{article}}%
\usepackage[T1]{{fontenc}}%
\usepackage[utf8]{{inputenc}}%
\usepackage{{lmodern}}%
\usepackage{{geometry}}%
\geometry{{margin=1.0in}}%
\usepackage{{hyperref}}%
\usepackage{{xcolor}}%
\pagestyle{{empty}}%

\begin{{document}}%
\noindent {{\fontsize{{22}}{{26}}\selectfont \textbf{{Sanshray Choudhary}}}} \vspace{{3pt}}\\%
\noindent \textbf{{\footnotesize sanshray.choudhary@gmail.com $\bullet$ +91 9810894391 $\bullet$ New Delhi, India}}\\%
\noindent \href{{https://www.linkedin.com/in/sanshray-choudhary-3591b9282}}{{linkedin.com/in/sanshray-choudhary-3591b9282}} $\bullet$ \href{{https://github.com/sanshraychoudhary-hue}}{{github.com/sanshraychoudhary-hue}} \vspace{{12pt}}%
\hrule \vspace{{18pt}}%

\noindent {date_str} \vspace{{12pt}}\\%
\noindent \textbf{{Hiring Team}} \\%
\noindent \textbf{{{company}}} \vspace{{16pt}}\\%

\noindent \textbf{{Subject: Application for {role} -- Sanshray Choudhary}} \vspace{{12pt}}\\%

\noindent Dear Hiring Team at {company}, \vspace{{8pt}}\\%

{body_content}

\noindent {company}'s commitment to engineering excellence and technological innovation makes this role an ideal match for my technical background and professional aspirations. I welcome the opportunity to discuss how my embedded development, hardware debugging, and systems engineering skills can deliver immediate value to your team. \vspace{{8pt}}\\%

\noindent Thank you for your time, consideration, and review of my application. \vspace{{18pt}}\\%

\noindent Sincerely, \vspace{{8pt}}\\%
\textbf{{Sanshray Choudhary}} \\%
sanshray.choudhary@gmail.com $\bullet$ +91 9810894391 \\%
\end{{document}}"""
    return letter_tex

def compile_latex(tex_path: str, output_dir: str) -> bool:
    """Compiles a .tex file to .pdf using pdflatex."""
    try:
        cmd = ["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", tex_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        return res.returncode == 0
    except Exception as e:
        print(f"Compilation error for {tex_path}: {e}")
        return False
