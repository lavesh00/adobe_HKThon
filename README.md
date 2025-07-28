
---

# 🏆 Adobe Hackathon 2025 - Solution

This repository contains the complete **Solution** for the **Adobe India Hackathon 2025: Connecting the Dots Challenge**.

---

## 🔍 Challenge Tracks

### ✅ Round 1A: PDF → JSON Extraction

* Extracts **document title**
* Detects **hierarchical headings** with level (H1, H2, etc.) and page number

### ✅ Round 1B: Multi-PDF Semantic Intelligence

* Accepts multiple PDFs + a **persona**
* Ranks sections based on **semantic similarity**
* Outputs **top 5 most relevant sections**
* Also generates **refined summaries**

---

## 🚀 Setup & Usage
```bash
 git clone https://github.com/lavesh00/adobe_HKThon.git
 cd adobe_HKThon
```

### 🐳 1. Docker Setup

#### 📦 Build Docker Image

```bash
docker build -t adobe-hackathon .
```

#### ▶️ Run Inside Docker

##### Round 1A:

**Bash/Linux/macOS:**

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  adobe-hackathon \
  --mode 1a \
  --input input/sample.pdf \
  --output output/result.json
```

**CMD (Windows):**

```cmd
docker run --rm ^
  -v %cd%\input:/app/input ^
  -v %cd%\output:/app/output ^
  --network none ^
  adobe-hackathon ^
  --mode 1a ^
  --input input/sample.pdf ^
  --output output/result.json
```

**PowerShell (Windows):**

```powershell
docker run --rm `
  -v ${PWD}/input:/app/input `
  -v ${PWD}/output:/app/output `
  --network none `
  adobe-hackathon `
  --mode 1a `
  --input input/sample.pdf `
  --output output/result.json
```

---

##### Round 1B:

**Bash/Linux/macOS:**

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  adobe-hackathon \
  --mode 1b \
  --input input/file01.pdf input/file02.pdf \
  --persona "Travel Planner" \
  --output output/1b.json
```

**CMD (Windows):**

```cmd
docker run --rm ^
  -v %cd%\input:/app/input ^
  -v %cd%\output:/app/output ^
  --network none ^
  adobe-hackathon ^
  --mode 1b ^
  --input input/file01.pdf input/file02.pdf ^
  --persona "Travel Planner" ^
  --output output/1b.json
```

**PowerShell (Windows):**

```powershell
docker run --rm `
  -v ${PWD}/input:/app/input `
  -v ${PWD}/output:/app/output `
  --network none `
  adobe-hackathon `
  --mode 1b `
  --input input/file01.pdf input/file02.pdf `
  --persona "Travel Planner" `
  --output output/1b.json
```

---

### 🖥️ 2. Python Local Setup

#### 💻 Environment Setup (Python 3.10+)

```bash
python -m venv venv
source venv/bin/activate        # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### ▶️ Run Locally

**Round 1A:**

```bash
python run.py --mode 1a --input input/sample.pdf --output output/result.json
```

**Round 1B:**

```bash
python run.py \
  --mode 1b \
  --input input/file01.pdf input/file02.pdf \
  --persona "Travel Planner" \
  --job "Plan a trip of 4 days for a group of 10 college friends." \
  --output output/1b.json
```

---

### 🧪 Run Tests

```bash
chmod +x scripts/test.sh
./scripts/test.sh
```

---

## 📤 Output Formats

### 🗂️ Round 1A Output (`--mode 1a`)

```json
{
  "title": "The Art of Travel",
  "outline": [
    { "text": "1. Introduction", "level": "H1", "page": 1 },
    { "text": "1.1 Purpose", "level": "H2", "page": 1 },
    { "text": "2. Destinations", "level": "H1", "page": 2 }
  ]
}
```

---

### 📘 Round 1B Output (`--mode 1b`)

```json
{
  "metadata": {
    "input_documents": ["file1.pdf", "file2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-07-28T20:05:00.000Z"
  },
  "extracted_sections": [
    {
      "document": "file2.pdf",
      "section_title": "Travel Tips",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "file2.pdf",
      "refined_text": "• Best time to visit is spring. • Use local buses or rental cars...",
      "page_number": 3
    }
  ]
}
```

---

## 📁 Directory Structure

```
├── input/                               # Folder for input PDF files
│   └── .gitkeep
├── output/                              # Folder for output JSON files
│   └── .gitkeep
├── src/                                 # Core source code
│   ├── models/                          # Custom model logic or downloaded models
│   │   ├── semantic_model.py            # Embedding & similarity (e.g., MiniLM)
│   │   └── heading_model.py             # Optional ML-based heading classifier (if any)
│   ├── round1a_processor.py             # Round 1A: Extracts title & structured outline
│   ├── round1b_processor.py             # Round 1B: Semantic matching across PDFs
│   ├── config.py                        # App-wide constants and paths
│   ├── heading_detector.py              # Rule-based heading detection via regex/text heuristics
│   ├── pdf_extractor.py                 # PDF → raw text (via PyMuPDF or OCR fallback)
│   ├── section_splitter.py              # Breaks PDF text into sections with page numbers
│   ├── intelligence_engine.py           # Handles semantic scoring (TF-IDF / MiniLM)
│   ├── summary_generator.py             # Extractive summary generator
│   └── utils.py                         # Common helpers (file ops, timing, logging)
├── monitoring/                          # Runtime monitoring and health checks
│   └── health.py                        # Health check endpoint or runtime diagnostics
├── scripts/                             # Shell scripts and utilities
│   ├── test.sh                          # Run full test suite (1A + 1B)
│   ├── benchmark.sh                     # Runtime & memory benchmarking
│   └── test_bench.sh                    # Custom test-bench execution for multiple PDFs
├── preload_model.py                     # CLI to preload MiniLM model for offline use
├── run.py                               # CLI entrypoint for Round1A & Round1B
├── Dockerfile                           # Docker setup (CPU-only, lightweight)
├── docker-compose.yml                   # Optional: for volume mapping & isolation
├── requirements.txt                     # Python dependencies
├── .gitignore                           # Ignored files/folders
└── README.md                            # 📘 Full documentation and usage

```
---
## Whole Working Logic in approach_explanation.md Please check it out there 

