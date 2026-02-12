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

Transform any YouTube video into a comprehensive, book-style summary using AI (Groq LLM).

## Features

- **🎬 Video to Summary**: Convert YouTube videos into detailed book-style summaries
- **🤖 AI-Powered**: Uses Groq's fast LLM for high-quality summaries
- **📝 Quick Bullet Summary**: TL;DR section with key takeaways
- **🌐 Multi-language Support**: Supports multiple transcript languages
- **🔑 Custom API Key**: Use your own Groq API key if rate limited

## How to Use

1. **Enter YouTube URL**: Paste any YouTube video URL
2. **Optional - Add API Key**: If the default key is rate-limited, add your own Groq API key
3. **Select Language**: Choose the transcript language (default: English)
4. **Generate**: Click "Generate Summary" and wait for the magic!

## Output Sections

The generated summary includes:
- **Executive Overview**: High-level summary of the content
- **Introduction**: Background and context
- **Chapter-by-Chapter Summary**: Detailed breakdown
- **Key Concepts and Definitions**: Important terms explained
- **Key Takeaways**: Numbered list of insights
- **Memorable Quotations**: Impactful quotes from the video
- **Practical Applications**: How to apply the learnings
- **Critical Analysis**: Strengths and limitations
- **Quick Bullet Summary (TL;DR)**: 5-10 bullet points for quick understanding

## Getting Your Own API Key

If the default API key is rate-limited:

1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Generate an API key
4. Paste it in the "Groq API Key" field

## Tech Stack

- **Frontend**: Gradio
- **Backend**: Python
- **AI**: Groq LLM (Llama 3.3 70B)
- **Transcript**: youtube-transcript-api

## License

MIT License
