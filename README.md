# YouTube to Book Summary Converter

Transform YouTube videos into comprehensive, book-style summaries using Groq's LLM API. This tool extracts transcripts and generates detailed summaries following a professional template.

## 🚀 Features

- **Automatic Transcript Extraction**: Fetches transcripts directly from YouTube videos
- **AI-Powered Summarization**: Uses Groq's Llama models for intelligent content analysis
- **Book-Style Output**: Generates structured summaries with chapters, key takeaways, quotes, and more
- **Long Video Support**: Handles long videos by intelligently chunking and processing
- **Multiple Output Formats**: Saves as well-formatted Markdown files
- **Batch Processing**: Process multiple videos at once
- **Interactive Mode**: Enter URLs one-by-one in interactive mode

## 📦 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd youtube_summary
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

4. **Add your Groq API key** to `.env`:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

   Get your API key from [Groq Console](https://console.groq.com/)

## 🎮 Usage

### Single Video

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

With options:
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --lang en \
  --verbose \
  --model llama-3.3-70b-versatile
```

### Interactive Mode

```bash
python main.py --interactive
```

### Batch Processing

Create a file `urls.txt` with URLs (one per line):
```
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
https://www.youtube.com/watch?v=VIDEO_ID_3
```

Then run:
```bash
python main.py --batch urls.txt
```

## 📖 Output Format

The generated summaries follow the book-style template with these sections:

1. **Executive Overview** - 2-3 paragraph summary of the content
2. **Introduction** - Background, presenter credentials, problem statement
3. **Chapter-by-Chapter Summary** - Detailed breakdown of content
4. **Key Concepts and Definitions** - Important terms explained
5. **Key Takeaways** - Numbered list of main insights
6. **Memorable Quotations** - 3-5 powerful quotes from the video
7. **Practical Applications** - How to apply the knowledge
8. **Critical Analysis** - Strengths, limitations, areas for deeper exploration
9. **Further Reading/Sources** - Resources mentioned
10. **Conclusion** - Synthesis and final thoughts

## ⚙️ Configuration

Edit `.env` to customize:

```env
# Groq API Configuration
GROQ_API_KEY=your_api_key_here

# Model selection
GROQ_MODEL=llama-3.3-70b-versatile

# Output directory
OUTPUT_DIR=./summaries
```

### Available Models

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `llama-3.3-70b-versatile` | Complex summaries | Fast | $$$ |
| `llama-3.1-8b-instant` | Quick summaries | Very Fast | $ |
| `mixtral-8x7b-32768` | Balanced | Fast | $$ |
| `gemma2-9b-it` | Creative content | Fast | $$ |

## 🏗️ Project Structure

```
youtube_summary/
├── main.py                 # CLI entry point
├── config.py              # Configuration management
├── youtube_transcript.py  # YouTube transcript extraction
├── groq_client.py         # Groq API client
├── summarizer.py          # Main summarization logic
├── youtube_summary.md     # Summary template
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## 🔧 Development

### Run Tests

```bash
python -m pytest
```

### Use as a Module

```python
from summarizer import YouTubeBookSummarizer

# Create summarizer
summarizer = YouTubeBookSummarizer()

# Generate summary
result = summarizer.summarize(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    verbose=True
)

if result['success']:
    print(result['summary'])
```

## ⚠️ Notes

- **Transcript Availability**: Not all YouTube videos have transcripts. The tool requires videos with available captions.
- **API Limits**: Groq has rate limits. For batch processing, consider adding delays.
- **Language Support**: Set `--lang` to your preferred language code (e.g., `es`, `fr`, `de`).
- **Long Videos**: Videos longer than ~25,000 characters are automatically chunked for processing.

## 📝 License

MIT License - feel free to use and modify.

## 🤝 Contributing

Pull requests welcome! Feel free to add features, fix bugs, or improve documentation.

---

Built with ❤️ using Groq API and youtube-transcript-api
