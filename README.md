# JobSearcher

JobSearcher is a self-hosted job search assistant and application package generator. It queries authentic corporate ATS requisitions and niche job portals, performs competency alignment against your master profile, verifies claims with a strict Fact Guard, tailors LaTeX resumes and cover letters, and serves a local web dashboard to manage applications from draft to interview.

---

## Key Highlights

- **Direct ATS Deep-Linking**: Connects with live portal feeds (FreeHire, OpenWeb Ninja / JSearch, and corporate career APIs) to ensure every job link points to a single, actionable vacancy rather than generic career hubs.
- **Fact Guard Verification**: Automatically cross-references metrics, project numbers, dates, and credentials against your master profile to eliminate hallucinated facts.
- **Native LaTeX PDF Generation**: Compiles professional PDF resumes and cover letters using local `pdflatex` from customizable `.tex` templates.
- **Self-Hosted Web GUI**: Local dashboard featuring Kanban board tracking (Draft, Applied, Screening, Interview, Offer, Rejected), split document view, and interactive AI refinement.

---

## Directory Structure

```text
JobSearcher/
├── applications/        # Generated application packets (PDFs, LaTeX, reports)
├── config.example.json  # Configuration template
├── my CV/               # Base LaTeX resume template and compiled PDF
├── profile/             # Master candidate profile and technical evidence
├── scripts/             # Core engines (portals, matcher, Fact Guard, LaTeX tailor)
│   ├── dossier_engine.py
│   ├── fact_guard.py
│   ├── job_portals.py
│   ├── latex_builder.py
│   ├── run_pipeline.py
│   └── search_and_extract.py
├── tracker/             # Markdown tracker and historical index
├── web/                 # Local Flask GUI backend and templates
├── start_gui.bat        # 1-click launcher for Windows
└── stop_gui.bat         # 1-click stop script
```

---

## Prerequisites

1. **Python 3.10+**
2. **LaTeX Engine (`pdflatex`)**:
   - Windows: [MiKTeX](https://miktex.org/) or TeX Live
   - Linux: `sudo apt install texlive-latex-base texlive-latex-extra`
   - macOS: `brew install --cask mactex`

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sanshraychoudhary-hue/JobSearcher.git
cd JobSearcher
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Configuration
Copy `config.example.json` to `config.json` and adjust your target roles, companies, and locations:
```bash
cp config.example.json config.json
```
- **FreeHire**: Works out of the box with zero API keys required.
- **Firecrawl / JSearch** *(Optional)*: Add your API keys if you wish to enable additional crawler providers.

### 4. Populate Your Master Profile
Edit `profile/master_profile.md` with your genuine education, projects, technical skills, and metrics. The Fact Guard uses this file as the ground truth.

---

## Usage

### Run the Discovery & Compilation Pipeline
To scan job portals, match requirements, and compile tailored LaTeX application packets:
```bash
python scripts/run_pipeline.py
```

### Launch the Web GUI
To inspect applications, view compiled PDFs, and refine documents in the browser:
- On Windows: Double-click `start_gui.bat`
- Or via terminal:
```bash
python web/app.py
```
Open **`http://localhost:5000`** in your browser.

---

## License

This project is open-source under the MIT License.
