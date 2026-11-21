# Master Career Profile — Sanshray Choudhary

---

## 1. Contact Information
- **Full Name**: Sanshray Choudhary
- **Email**: sanshray.choudhary@gmail.com
- **Phone**: +91 9810894391
- **Location**: New Delhi / Dwarka, India (Open to Remote / Hybrid / Relocation)
- **LinkedIn**: https://www.linkedin.com/in/sanshray-choudhary-3591b9282
- **GitHub**: https://github.com/sanshraychoudhary-hue

---

## 2. Professional Summary
Innovative Electronics & Communication Engineering professional and Embedded Systems Developer with deep hands-on expertise in **ARM Cortex (STM32), ESP32-S3, dual-core FreeRTOS, real-time DSP, and custom PCB design (KiCad)**. Proven track record building production-grade industrial IoT nodes, bioacoustic detectors, autonomous robotics (ROS 2), and edge AI (TinyML/TFLite) with sub-50ms latency. Recognized by IIT Bombay (e-Yantra Level 3, Embedded Systems & ROS 2 Certified) and top national hackathons. Passionate about industrial automation, functional safety (IEC 61508 SIL 2), protocol implementation (CAN, Modbus, RS-485, I2S, SPI), and firmware development for mission-critical applications at companies like Siemens, Honeywell, and Schneider Electric.

---

## 3. Core Competencies & Technical Skills

### Core Electronics & Embedded Systems
- **Microcontrollers & Processors**: ARM Cortex-M3/M4, ARM V7, STM32 (STM32F407, STM32F401VE), ESP32 / ESP32-S3 (Dual-Core, Octal PSRAM), Raspberry Pi Pico W, Arduino AVR, Microchip/Atmel.
- **Real-Time Systems & Architecture**: FreeRTOS (Dual-core task scheduling, queues, semaphores, circular DMA buffers, power management, deep sleep modes).
- **Communication Protocols & Buses**: SPI, I2C, I2S (DMA streaming), UART, CAN Bus, RS-485, Modbus, MQTT, GPIO, WDT, Timers, Bluetooth, Wi-Fi.
- **Hardware & PCB Design**: KiCad (Schematic capture, multi-layer high-speed layout, 0 DRC violations, BOM optimization), Circuit Design, Power Electronics, Logic Analyzers, Oscilloscopes, Hardware Debugging.
- **Signal Processing & Optical Sensing**: Real-time DSP (Radix-4 FFT, Quadrature Heterodyne Down-Conversion, Digital Filtering), Laser Spectroscopy & Optical Sensing, Laser Driver Development (TEC).
- **Robotics & Control Systems**: ROS / ROS 2, PID Motion Control, Sensors & Actuators integration, CoppeliaSim simulation, Omni-directional kinematics (Mecanum).
- **Functional Safety & Standards**: Familiarity with IEC 61508 SIL 2 functional safety standards.
- **FPGA & Hardware Description**: FPGA Design, VHDL, Verilog.

### Software Development & Computing
- **Programming Languages**: C, C++, Python, MATLAB, SQL (MySQL).
- **Embedded Toolchains & IDEs**: STM32CubeIDE / STM32CubeMX, IAR Embedded Workbench, MPLAB, Eclipse, Arduino IDE.
- **AI/ML & Edge Computing**: TinyML, TensorFlow, TensorFlow Lite (Micro), OpenCV, Embedded AI, Tensor Cores / NPUs, Computer Vision.
- **Web & Mobile Tools**: React.js, Flutter, Firebase, REST APIs.
- **Version Control & Quality**: Git, GitHub, Unit Testing, Minitab.

### Mechanical & Other Skills
- **3D Modeling & Fabrication**: Autodesk Fusion 360, 3D Printing / Prototyping, CNC Machining.
- **Leadership & Communication**: Technical Writing, Event Management, Public Speaking.

---

## 4. Education

- **Bachelor of Technology (B.Tech) in Electronics and Communication Engineering**  
  *University School of Information, Communication and Technology (USICT), Dwarka, Delhi* | *2023 – 2027*  
  **GPA: 8.42 / 10.0**

- **Senior Secondary (Class XII - PCM), CBSE**  
  *The Air Force School, Subroto Park, Delhi Cantt* | *2022*  
  **Percentage: 93.8%**

- **Secondary (Class X), CBSE**  
  *The Air Force School, Subroto Park, Delhi Cantt* | *2020*  
  **Percentage: 94.6%**

---

## 5. Licenses & Certifications

- **e-Yantra Robotics Competition (Level 3)** — *Issued by e-Yantra, IIT Bombay* (Mar 2025)
- **ROS 2 Developer** — *Issued by e-Yantra, IIT Bombay* (Feb 2025)
- **Embedded Systems Developer** — *Issued by e-Yantra, IIT Bombay* (Dec 2024)

---

## 6. Professional Experience

### Winter Intern — India Space Academy
*Feb 2026 – Mar 2026*
- Developed embedded firmware for advanced drone technology utilizing microcontrollers, I2C/SPI interfaces, and optimized power management.
- Implemented robust fail-safes and real-time sensor polling routines for flight stability.

### Internship Trainee — BSNL
*Jun 2026 – Jul 2026*
- Underwent practical industrial training on telecommunications infrastructure, digital switching systems, and high-reliability network transmission lines.

### Project Intern — AICTE (Project OmniServe)
*Jun 2025 – Aug 2025*
- Engineered an autonomous Wi-Fi controlled omni-directional mobile robot platform using Raspberry Pi Pico W, mecanum wheels, and closed-loop encoder PID motion control.

### Project Intern — AICTE (Project Sanchalak Kavach)
*Jun 2024 – Aug 2024*
- Designed and fabricated a smart safety helmet attachment integrating ESP32, HUD navigation, crash detection algorithms (MPU6050, BMP280), and automatic SMS alert dispatch.

### Leadership & Community Roles
- **Joint Secretary — TechSpace** (*Nov 2024 – Present*): Facilitated technical events, embedded systems bootcamps, and robotics seminars for 500+ student developers.
- **Lens Coordinator & Devsource Operations — GGSIPU USS ACM Student Chapter** (*Apr 2024 – Present*).
- **Member — USICT Alumni Committee** (*Apr 2024 – Present*).
- **Flautist — SWAR GGSIPU** (*Nov 2023 – Present*).

---

## 7. Featured Engineering Projects

### AtiDhwani — ESP32-S3 Ultrasonic Bat PAM Node & Bioacoustics Detector
*Nov 2026 – Present* | *Embedded C, FreeRTOS, KiCad, DSP, ESP-IDF*
- Engineered an open-source modular Passive Acoustic Monitoring (PAM) node and handheld detector capturing 10–96 kHz wildlife bioacoustics with continuous 192 kHz / 24-bit sampling at < $40 BOM (replacing $1,000–$3,500 industrial gear).
- Developed dual-core FreeRTOS firmware on ESP32-S3 (240 MHz, 8MB Octal PSRAM): Core 0 manages high-speed DMA I2S streaming and drop-free FAT32 WAV logging to MicroSD via a 3.6MB circular PSRAM buffer.
- Implemented real-time DSP on Core 1 executing quadrature heterodyne down-conversion (tunable 15–90 kHz LO), frequency division, and 128-point Radix-4 FFT spectral analysis displayed on a 0.91" SSD1306 OLED at 30 FPS.
- Designed custom 2-layer carrier PCB in KiCad (0 DRC violations) integrating dual MEMS microphones, ultra-low-noise LDO, 24-bit Wolfson WM8782 stereo ADC (Master Mode, 24.576 MHz crystal), and 32-bit TI PCM5102A DAC driving field headphones with zero perceived latency.

### STM32 Industrial IoT Sensor Hub
*Jan 2025* | *STM32F407, FreeRTOS, C/C++, MQTT, KiCad*
- Developed an industrial-grade sensor node using STM32F407 interfacing with SPI-based ADCs, I2C temperature sensors, and UART industrial gas sensors.
- Authored lightweight FreeRTOS firmware managing concurrent sensor sampling, digital filtering, and reliable MQTT transmission via an ESP8266 Wi-Fi module.
- Engineered intelligent deep-sleep power management algorithms, maximizing operational lifespan in remote battery-powered deployments.

### Aegis Guardian — AI Fall Detection & Health Monitoring System
*Oct 2025* | *ESP32, Python, TinyML/TFLite, I2C, MQTT*
- Engineered an ESP32 wearable embedded system for real-time fall detection and physiological telemetry.
- Developed low-overhead firmware for 50Hz sensor acquisition (MPU6050, AD8232 ECG, BMP180) via I2C/ADC with optimized Wi-Fi streaming.
- Trained and deployed a multi-model pipeline (Random Forest + TFLite CNN) achieving 99.97% accuracy with sub-50ms latency.

### OmniServe Autonomous Mobile Robot
*Jun 2025* | *Raspberry Pi Pico W, C/C++, Python, WebSockets, PID*
- Built an autonomous omni-directional mobile robot utilizing 4-wheel Mecanum drive and optical encoder PID feedback, achieving centimeter-level waypoint accuracy.
- Created a live browser-based telemetry dashboard and integrated a 4-DOF robotic arm for automated pick-and-place routines.

### Portable EMI/EMC Detection Machine — SIH 2024
*Jun 2024* | *STM32F401VE, Analog Signal Processing, Embedded C*
- Developed a portable EMI/EMC meter tailored for metropolitan transit networks using STM32F401VE, AD633 multiplier, LMF380 filter, and OLED display for field wireless electromagnetic interference monitoring.

### AI Acoustic Railway Crack Monitoring — SIH 2024
*Jun 2024* | *FPGA, Autoencoders, Reinforcement Learning, Signal Processing*
- Designed an intelligent railway inspection system fusing Station-Based Acoustic Systems (SBAS) and onboard vibration sensors with FPGA processing and autoencoders for real-time rail crack identification.

### SonicBeam Personalised Audio Guidance
*Jul 2025* | *Python, OpenCV, Embedded C, FM RF*
- Built an assistive directional audio system combining OpenCV computer-vision tracking in Python with an FM directional audio beam for non-intrusive accessibility cues.

### Self-Balancing Bot — e-Yantra 2024
*Sep 2024* | *Arduino Nano, MPU6050, PID Control, CoppeliaSim*
- Developed a two-wheeled inverted pendulum self-balancing robot with custom PID control algorithms; modeled and simulated dynamics in Python & CoppeliaSim.

---

## 8. Honors & Awards
- **2nd Position** — Innoverse’36 Hackathon (Issued by SGT University Gurgaon, Feb 2025)
- **1st Prize** — IIITD Odyssey’24 (Rogue Renders, IIIT-Delhi)
- **1st Prize** — CBSE State & Regional Level Science Exhibition
- **National Participant** — CBSE National Level Science Exhibition
