import pylatex
from pylatex import Document, Command, NoEscape

def generate_resume():
    geometry_options = {"margin": "0.7in"}
    doc = Document(documentclass='article', document_options=['10pt', 'a4paper'], geometry_options=geometry_options)
    
    # Packages
    doc.preamble.append(Command('usepackage', 'enumitem'))
    doc.preamble.append(Command('usepackage', 'hyperref'))
    doc.preamble.append(Command('usepackage', 'titlesec'))
    doc.preamble.append(Command('usepackage', 'xcolor'))
    
    # Custom formatting
    doc.preamble.append(NoEscape(r'\titleformat{\section}{\large\bfseries\uppercase}{}{0em}{}[\titlerule]'))
    doc.preamble.append(NoEscape(r'\titlespacing{\section}{0pt}{12pt}{8pt}'))
    
    # Disable page numbers
    doc.preamble.append(Command('pagestyle', 'empty'))
    
    # Header
    doc.append(NoEscape(r'\noindent {\fontsize{28}{34}\selectfont \textbf{Sanshray Choudhary}} \vspace{3pt}\\'))
    doc.append(NoEscape(r'\noindent \textbf{\scriptsize sanshray.choudhary@gmail.com $\bullet$ +91 9810894391 $\bullet$ \href{https://www.linkedin.com/in/sanshray-choudhary-3591b9282}{https://www.linkedin.com/in/sanshray-choudhary-3591b9282} \\ \href{https://github.com/sanshraychoudhary-hue}{https://github.com/sanshraychoudhary-hue}} \vspace{10pt}'))
    
    # EDUCATION
    doc.append(NoEscape(r'\section*{Education}'))
    doc.append(NoEscape(r'\noindent \textbf{University School of Information, Communication and Technology, Dwarka - 110078} \hfill 2023--2027 \\'))
    doc.append(NoEscape(r'\indent \textit{Bachelor of Technology, Electronics and Communication Engineering (8.42 GPA)} \vspace{8pt}\\'))
    
    doc.append(NoEscape(r'\noindent \textbf{The Air Force School, Subroto Park, Delhi Cantt - 110010} \hfill 2009--2022 \\'))
    doc.append(NoEscape(r'\indent \textit{Senior Secondary (XII) (PCM), CBSE (93.8\%)} \\'))
    doc.append(NoEscape(r'\indent \textit{Secondary (X), CBSE (94.6\%)} \vspace{8pt}'))

    # LICENSES & CERTIFICATIONS
    doc.append(NoEscape(r'\section*{Licenses \& Certifications}'))
    doc.append(NoEscape(r'\noindent \textbf{e-Yantra Robotics Competition (Level 3)} \hfill Mar 2025 \\'))
    doc.append(NoEscape(r'\indent \textit{Issued by e-Yantra, IIT Bombay} \vspace{8pt}\\'))
    
    doc.append(NoEscape(r'\noindent \textbf{ROS 2 Developer} \hfill Feb 2025 \\'))
    doc.append(NoEscape(r'\indent \textit{Issued by e-Yantra, IIT Bombay} \vspace{8pt}\\'))
    
    doc.append(NoEscape(r'\noindent \textbf{Embedded Systems Developer} \hfill Dec 2024 \\'))
    doc.append(NoEscape(r'\indent \textit{Issued by e-Yantra, IIT Bombay} \vspace{8pt}'))
    
    # PROFESSIONAL EXPERIENCE
    doc.append(NoEscape(r'\section*{Professional Experience}'))

    doc.append(NoEscape(r'\noindent \textbf{Internship Trainee, BSNL} \hfill Jun 2026 -- Jul 2026 \vspace{8pt}\\'))
    
    doc.append(NoEscape(r'\noindent \textbf{Winter Intern, India Space Academy} \hfill Feb 2026 -- Mar 2026'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Developed embedded firmware for advanced drone technology utilizing microcontrollers, I2C/SPI interfaces, and optimized power management.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Project Intern, AICTE} \hfill Jun 2025 -- Aug 2025'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Project mentioned in Projects \& Extracurricular Section (OmniServe)'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))
    
    doc.append(NoEscape(r'\noindent \textbf{TechSpace, Joint Secretary} \hfill Nov 2024 -- Present'))
    doc.append(NoEscape(r'\noindent \textbf{TechSpace, Joint Secretary} \hfill Sep 2025 -- May 2026'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Facilitated technical events, workshops, and embedded systems seminars to foster peer-to-peer technical growth.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Project Intern, AICTE} \hfill Jun 2024 -- Aug 2024'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Project mentioned in Projects \& Extracurricular Section (Smart Helmet)'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))
    
    doc.append(NoEscape(r'\noindent \textbf{GGSIPU USS ACM Student Chapter} \hfill Apr 2024 -- Present'))
    doc.append(NoEscape(r'\noindent \textbf{GGSIPU USS ACM Student Chapter} \hfill Apr 2024 -- May 2026'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Lens -- Coordinator \& Core Team Member; Devsource Operations Member'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))
    
    doc.append(NoEscape(r'\noindent \textbf{USICT Alumni Committee, Member} \hfill Apr 2024 -- Present \vspace{8pt}\\'))
    doc.append(NoEscape(r'\noindent \textbf{SWAR GGSIPU, Flautist} \hfill Nov 2023 -- Present \vspace{8pt}'))
    doc.append(NoEscape(r"\noindent \textbf{Institution's Innovation Council (IIC), GGSIPU, Member} \hfill Nov 2025 -- Present \vspace{8pt}\\"))
    doc.append(NoEscape(r'\noindent \textbf{USICT Alumni Committee, Member} \hfill Apr 2024 -- Feb 2026 \vspace{8pt}\\'))
    doc.append(NoEscape(r'\noindent \textbf{SWAR GGSIPU, Flautist} \hfill Nov 2023 -- May 2026 \vspace{8pt}'))

    # PROJECTS
    doc.append(NoEscape(r'\section*{Projects \& Extracurricular}'))
    doc.append(NoEscape(r'\newpage \section*{Projects \& Extracurricular}'))
    
    doc.append(NoEscape(r'\noindent \textbf{AtiDhwani -- ESP32-S3 Ultrasonic Bat PAM Node \& Bioacoustics Detector} \hfill Nov 2026 -- Present'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Engineered an open-source modular Passive Acoustic Monitoring (PAM) node and handheld bat detector capturing 10--96\,kHz wildlife bioacoustics with 192\,kHz / 24-bit continuous sampling at $<$ \$40 BOM cost (vs.\ \$1,000--\$3,500 commercial systems).'))
    doc.append(NoEscape(r'\item Developed dual-core FreeRTOS firmware on ESP32-S3 (240\,MHz, 8MB Octal PSRAM): Core 0 manages high-speed DMA I2S streaming and drop-free FAT32 WAV logging to MicroSD via a 3.6MB circular PSRAM buffer.'))
    doc.append(NoEscape(r'\item Implemented real-time DSP on Core 1 executing quadrature heterodyne down-conversion (tunable 15--90\,kHz LO), frequency division, and 128-point Radix-4 FFT spectral analysis displayed on a 0.91" SSD1306 OLED at 30\,FPS.'))
    doc.append(NoEscape(r'\item Designed custom 2-layer carrier PCB in KiCad (0 DRC violations) integrating dual MEMS microphones, ultra-low-noise LDO, 24-bit Wolfson WM8782 stereo ADC (Master Mode, 24.576\,MHz crystal), and 32-bit TI PCM5102A DAC driving field headphones with zero perceived latency.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Aegis Guardian - AI Fall Detection \& Health Monitoring System} \hfill Oct 2025'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Engineered an ESP32-based embedded wearable system for real-time fall detection and vital monitoring.'))
    doc.append(NoEscape(r'\item Developed firmware for 50Hz sensor acquisition (MPU6050, AD8232, BMP180) using I2C/ADC with optimized Wi-Fi data streaming to a Python ML inference server.'))
    doc.append(NoEscape(r'\item Implemented a multi-model pipeline (Random Forest + TFLite CNN) achieving 99.97\% accuracy with sub-50ms latency, and integrated cloud sync for remote monitoring.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{SonicBeam Personalised Audio} \hfill Jul 2025'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Developed an embedded assistive guidance system leveraging FM-based directional audio amplification for personalized, non-intrusive audio cues.'))
    doc.append(NoEscape(r'\item Integrated embedded hardware with OpenCV-based computer vision in Python for real-time user detection and location awareness, targeting accessibility applications.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{OmniServe (Internship Project)} \hfill Jun 2025'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Developed an autonomous Wi-Fi controlled omni-directional mobile robot using Raspberry Pi Pico W with mecanum wheels, encoder-based PID motion control, and centimeter-level navigation accuracy.'))
    doc.append(NoEscape(r'\item Implemented a web-based control dashboard with real-time telemetry and integrated a robotic arm for basic pick-and-place operations, validated under real-world load conditions.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Solar Tracker} \hfill May 2025'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Designed a solar tracker system using 4 LDRs and a servo motor to dynamically align the panel for maximum sunlight exposure.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Aero} \hfill Feb 2025'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Created an ESP32-based IoT system to collect air quality data, store it in Firebase, and use AI models to recommend tree species for pollution control. Secured 2nd place at Innoverse\'36.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{STM32 Industrial IoT Sensor Hub} \hfill Jan 2025'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Developed a high-performance industrial sensor node using STM32F407, interfacing with SPI-based ADCs, I2C temperature sensors, and UART gas sensors.'))
    doc.append(NoEscape(r'\item Implemented a lightweight FreeRTOS firmware to manage concurrent sensor sampling, data filtering, and reliable MQTT transmission over an ESP8266 Wi-Fi module.'))
    doc.append(NoEscape(r'\item Designed an intelligent power management algorithm using deep sleep modes to maximize battery life in remote deployments.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{ESP32 Tetris (VGA compatible)} \hfill Sep 2024'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Developed a playable Tetris game using ESP32 and VGA output, programming game logic, collision detection, and responsive controls in Arduino IDE.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Self-Balancing Bot - eYantra 2024 (Stage 1 – Qualified)} \hfill Sep 2024'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Built a self-balancing robot using an Arduino Nano, MPU6050, and encoders. Tuned the PID controller and simulated in Python/CoppeliaSim.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Portable EMI/EMC detection machine - SIH 2024} \hfill Jun 2024'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Developed a portable EMI/EMC meter for metro networks using STM32F401VE, AD633, LMF380, and OLED12864, featuring onboard sensors and wireless monitoring.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{AI Acoustic Railway Monitoring - SIH 2024} \hfill Jun 2024'))
    doc.append(NoEscape(r'\newpage \noindent \textbf{AI Acoustic Railway Monitoring - SIH 2024} \hfill Jun 2024'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Combined Station-Based Acoustic Systems (SBAS) and onboard sensors for real-time railway crack detection using autoencoders, reinforcement learning, and FPGA.'))
    doc.append(NoEscape(r'\item Predicted cracks for preventive maintenance, improving railway safety and efficiency.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Sanchalak Kavach (Smart Helmet) (Internship Project)} \hfill Jun 2024'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Built a smart helmet attachment with HUD navigation, crash detection (MPU6050, BMP280), and SMS alerts via ESP32.'))
    doc.append(NoEscape(r'\item Integrated Bluetooth for Android, built-in ventilation, vibration motors, and speakers, featuring an AI-based crash prediction model.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{CNC Plotter} \hfill Apr 2024'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Built a compact CNC plotter capable of precise 2D drawing using stepper motors and an Arduino-based control system.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    doc.append(NoEscape(r'\noindent \textbf{Line Following Robot (LFR)} \hfill Mar 2024'))
    doc.append(NoEscape(r'\begin{itemize}[leftmargin=15pt, nosep, topsep=0pt]'))
    doc.append(NoEscape(r'\item Developed a Line Following Robot using a PID algorithm. Designed a custom 3D-printed chassis with 7 IR sensors, powered by an Arduino Nano.'))
    doc.append(NoEscape(r'\end{itemize} \vspace{8pt}'))

    # AWARDS
    doc.append(NoEscape(r'\section*{Awards}'))
    doc.append(NoEscape(r'\noindent \textbf{Innoverse’36 Hackathon -- 2nd Position}: Issued by SGT University Gurgaon \vspace{8pt}\\'))
    doc.append(NoEscape(r'\noindent \textbf{IIITD Odyssey\'24 - Rogue Renders -- 1st prize}: Issued by IIIT-D \vspace{8pt}\\'))
    doc.append(NoEscape(r'\noindent \textbf{CBSE National Level Science Exhibition}: Participation \vspace{8pt}\\'))
    doc.append(NoEscape(r'\noindent \textbf{CBSE State and Regional Level Science Exhibition -- 1st prize}: Issued by CBSE \vspace{8pt}'))

    # SKILLS
    doc.append(NoEscape(r'\section*{Skills}'))
    doc.append(NoEscape(r'\noindent \textbf{Core Electronics \& Embedded Systems:} Microcontrollers (ARM Cortex M3/M4, ARM V7, STM32, ESP32, Arduino), IoT, Robotics, Signal Processing (FFT, Filtering), Digital Electronics, Circuit Design, PCB Design (KiCad), FreeRTOS, Sensors \& Actuators, Control Systems, PID Control, Reinforcement Learning (for embedded AI), Power Electronics, CNC Machining, STM32Cube, Arduino AVR, FPGA Design (VHDL/Verilog), High-Speed Data Acquisition (ADC, DMA), Functional Safety (IEC 61508 SIL 2), Protocols \& Interfaces (SPI, I2C, I2S, UART, CAN, RS-485, Modbus, MQTT, GPIO, WDT, TIMER), Laser Spectroscopy \& Optical Sensing, Laser Driver Dev (TEC), Hardware Debugging (Logic Analyzers) \vspace{8pt}\\'))
    doc.append(NoEscape(r'\noindent \textbf{Computer \& Software Development:} C, C++, Python, MATLAB, Minitab, IAR Embedded Workbench, Eclipse, MPLAB, Web Development (React.js, Flutter, Firebase), AI/ML \& Edge Computing (TensorFlow, TensorFlow Lite, OpenCV, TinyML, Embedded AI, Tensor Cores, NPUs), Git, MySQL, Simulation \& Modelling, CoppeliaSim \vspace{8pt}\\'))
    doc.append(NoEscape(r'\noindent \textbf{Other Skills:} 3D Modelling (Fusion 360), ROS/ROS2 (Robot Operating System), Technical Writing, Photography, Graphic Design, Public Speaking, Event Management'))

    doc.generate_pdf('Sanshray_Choudhary_Updated_CV', compiler='pdflatex', clean_tex=False)

if __name__ == '__main__':
    generate_resume()
