# 🎯 YouTube to Book Summary - Complete Guide

This guide covers both **local installation** and **Hugging Face deployment**.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Installation](#local-installation)
3. [Running Locally (CLI)](#running-locally-cli)
4. [Running Locally (Gradio Web UI)](#running-locally-gradio-web-ui)
5. [Hugging Face Deployment](#hugging-face-deployment)
6. [Usage Examples](#usage-examples)
7. [Troubleshooting](#troubleshooting)

---

## 📋 Prerequisites

Before installing, ensure you have:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Package manager (comes with Python)
- **Groq API Key** - [Get one free](https://console.groq.com/)
- **Git** - For Hugging Face deployment

---

## 💻 Local Installation

### Step 1: Clone/Download the Project

```bash
# If from Git
git clone <repository-url>
cd youtube_summary

# Or navigate to the project directory
cd path/to/youtube_summary
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

### Step 4: Configure API Key

**Option A: Using .env file (Recommended)**

1. Copy the template:
   ```bash
   copy .env.example .env   # Windows
   cp .env.example .env     # Linux/macOS
   ```

2. Edit `.env` file:
   ```
   GROQ_API_KEY=gsk_your_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   OUTPUT_DIR=./summaries
   ```

**Option B: Set environment variable temporarily**

Windows (Command Prompt):
```cmd
set GROQ_API_KEY=gsk_your_api_key_here
```

Windows (PowerShell):
```powershell
$env:GROQ_API_KEY="gsk_your_api_key_here"
```

Linux/macOS:
```bash
export GROQ_API_KEY="gsk_your_api_key_here"
```

---

## 🖥️ Running Locally (CLI)

### Quick Start

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `URL` | YouTube video URL |
| `--lang, -l` | Language code (default: en) |
| `--model, -m` | Groq model to use |
| `--no-save` | Don't save output to file |
| `--verbose, -v` | Show detailed progress |
| `--batch, -b` | Process URLs from file |
| `--interactive, -i` | Interactive mode |

### Examples

```bash
# Basic usage
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# With verbose output
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --verbose

# Different language
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang es

# Batch processing
python main.py --batch urls.txt

# Interactive mode
python main.py --interactive
```

---

## 🌐 Running Locally (Gradio Web UI)

### Start the Web Interface

```bash
python app.py
```

### Access the Interface

1. Open your browser
2. Go to: `http://localhost:7860`

### Features

- **Modern dark theme** with gradient design
- **YouTube URL input** with validation
- **Optional API Key** - Override the default key if rate-limited
- **Language selection** dropdown
- **Progress tracking** during generation
- **Video information display**
- **Example videos** for quick testing

### Using Custom API Key in Web UI

1. Click "⚙️ Advanced Settings"
2. Enter your Groq API key
3. The app will use your key instead of the default

---

## 🤗 Hugging Face Deployment

### Step 1: Create Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co/)
2. Sign up for a free account
3. Verify your email

### Step 2: Create a New Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in the details:
   - **Space name**: `youtube-to-book-summary` (or your choice)
   - **License**: MIT
   - **SDK**: Select **Gradio**
   - **Hardware**: CPU (free) or upgrade for better performance
3. Click "Create Space"

### Step 3: Upload Files

**Method A: Using Git (Recommended)**

```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/youtube-to-book-summary
cd youtube-to-book-summary

# Copy all project files
copy /path/to/youtube_summary/* .

# Or copy specific required files:
# - app.py
# - requirements.txt
# - config.py
# - summarizer.py
# - youtube_transcript.py
# - groq_client.py
# - youtube_summary.md
# - utils/ folder

# Create README.md for HF (use the template below)
# Then commit and push
git add .
git commit -m "Initial deployment"
git push
```

**Method B: Using Web Interface**

1. Go to your Space page
2. Click "Files" → "Add file" → "Upload files"
3. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `config.py`
   - `summarizer.py`
   - `youtube_transcript.py`
   - `groq_client.py`
   - `youtube_summary.md`
   - `utils/__init__.py`
   - `utils/statistics.py`

### Step 4: Create README.md for Hugging Face

Create a `README.md` file with this content:

```markdown
---
title: YouTube to Book Summary
emoji: 📚
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 📚 YouTube to Book Summary Converter

Transform any YouTube video into a comprehensive, book-style summary using AI.

## Features

- 🎬 Convert YouTube videos to detailed summaries
- 🤖 AI-powered using Groq LLM
- 📝 Quick bullet summary (TL;DR)
- 🌐 Multi-language support
- 🔑 Custom API key support

## Usage

1. Enter a YouTube URL
2. (Optional) Add your Groq API key if rate-limited
3. Click "Generate Summary"

## Get API Key

Visit [console.groq.com](https://console.groq.com/) for a free API key.
```

### Step 5: Set Environment Variables (Secret)

1. Go to your Space → **Settings**
2. Scroll to **Repository Secrets**
3. Click "New secret"
4. Add:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your Groq API key
5. Click "Save"

### Step 6: Verify Deployment

1. Wait 2-5 minutes for build to complete
2. Check the "Logs" tab for any errors
3. Your app should be live at:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/youtube-to-book-summary
   ```

### Required Files for Hugging Face

```
youtube-to-book-summary/
├── app.py              # Main Gradio app
├── requirements.txt    # Python dependencies
├── README.md           # HF metadata (with YAML header)
├── config.py           # Configuration
├── summarizer.py       # Summary generation
├── youtube_transcript.py  # Transcript extraction
├── groq_client.py      # Groq API client
├── youtube_summary.md  # Prompt template
└── utils/
    ├── __init__.py
    └── statistics.py
```

---

## 📖 Usage Examples

### Example 1: Basic Summary

```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Example 2: Verbose Mode

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --verbose
```

### Example 3: Batch Processing

Create `urls.txt`:
```
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
https://www.youtube.com/watch?v=VIDEO_ID_3
```

Run:
```bash
python main.py --batch urls.txt
```

### Example 4: Different Model

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --model llama-3.1-8b-instant
```

---

## 🔧 Troubleshooting

### Error: "GROQ_API_KEY not found"

**Solution:**
1. Check if `.env` file exists
2. Verify API key is correctly set
3. Restart terminal after setting environment variables

### Error: "No transcripts available"

**Cause:** Video doesn't have captions enabled.

**Solutions:**
- Try a different video with captions
- Check if video is region-restricted

### Error: "Rate limit exceeded"

**Solutions:**
- Wait a few minutes and retry
- Use your own API key in the web UI
- Use a different model: `--model llama-3.1-8b-instant`

### Hugging Face: Build Error

**Solutions:**
1. Check the Logs tab for specific errors
2. Ensure all required files are uploaded
3. Verify `requirements.txt` has correct dependencies
4. Make sure `GROQ_API_KEY` secret is set

### Hugging Face: App Not Loading

**Solutions:**
1. Check if build completed successfully
2. Verify `app_file: app.py` in README.md header
3. Check for Python errors in Logs

---

## 📊 Model Comparison

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `llama-3.3-70b-versatile` | Complex summaries | Fast | $$$ |
| `llama-3.1-8b-instant` | Quick summaries | Very Fast | $ |
| `mixtral-8x7b-32768` | Balanced | Fast | $$ |

---

## 📁 Output Files

Summaries are saved to `./summaries/`:

```
summaries/
├── Video_Title_VIDEO_ID_book_20240115_120000.docx
├── Video_Title_VIDEO_ID_book_20240115_120000.pdf
└── Video_Title_VIDEO_ID_transcript_20240115_120000.docx
```

---

## ✅ Quick Reference

### Local CLI
```bash
# Install
pip install -r requirements.txt

# Configure
copy .env.example .env
# Edit .env and add GROQ_API_KEY

# Run
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Local Web UI
```bash
# Start Gradio app
python app.py

# Open browser to http://localhost:7860
```

### Hugging Face Deploy
```bash
# Clone space
git clone https://huggingface.co/spaces/YOUR_USERNAME/your-space-name

# Copy files and push
git add .
git commit -m "Deploy"
git push
```

---

**Happy summarizing! 📚✨**
