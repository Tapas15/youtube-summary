"""
Gradio Frontend for YouTube to Book Summary Converter
Deploy on Hugging Face Spaces
"""
import os
import gradio as gr
from datetime import datetime
from typing import Optional, Tuple

# Import our modules
from config import config
from summarizer import YouTubeBookSummarizer, create_summarizer
from youtube_transcript import YouTubeExtractor, extract_transcript


# Custom CSS for attractive design
CUSTOM_CSS = """
/* Main container styling */
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    min-height: 100vh;
}

/* Header styling */
.app-header {
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
}

.app-header h1 {
    color: white !important;
    font-size: 2.5em !important;
    margin-bottom: 10px !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.app-header p {
    color: rgba(255,255,255,0.9) !important;
    font-size: 1.1em !important;
}

/* Input container styling */
.input-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

/* Text input styling */
input[type="text"], textarea {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 1em !important;
    transition: all 0.3s ease !important;
}

input[type="text"]:focus, textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
}

input[type="text"]::placeholder, textarea::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
}

/* Button styling */
.primary-btn {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 1.1em !important;
    font-weight: 600 !important;
    padding: 15px 30px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4) !important;
}

.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6) !important;
}

/* Output container styling */
.output-container {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 15px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    margin-top: 20px;
}

/* Markdown output styling */
.markdown-text {
    color: #e0e0e0 !important;
    line-height: 1.8 !important;
}

.markdown-text h1 {
    color: #667eea !important;
    border-bottom: 2px solid rgba(102, 126, 234, 0.3) !important;
    padding-bottom: 10px !important;
}

.markdown-text h2 {
    color: #a78bfa !important;
}

.markdown-text h3 {
    color: #c4b5fd !important;
}

.markdown-text ul, .markdown-text ol {
    color: #e0e0e0 !important;
}

/* Status message styling */
.status-success {
    background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    padding: 15px !important;
    border-radius: 10px !important;
    margin: 10px 0 !important;
}

.status-error {
    background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
    color: white !important;
    padding: 15px !important;
    border-radius: 10px !important;
    margin: 10px 0 !important;
}

.status-info {
    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    padding: 15px !important;
    border-radius: 10px !important;
    margin: 10px 0 !important;
}

/* Accordion styling */
.accordion {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    margin: 10px 0 !important;
}

/* Label styling */
label {
    color: #c4b5fd !important;
    font-weight: 500 !important;
}

/* Examples section */
.examples-container {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    padding: 15px;
    margin-top: 20px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.9em;
}

/* Loading animation */
.loading {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #667eea, #764ba2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #764ba2, #667eea);
}
"""


def process_video(
    url: str,
    api_key: Optional[str] = None,
    language: str = "en",
    progress: gr.Progress = gr.Progress()
) -> Tuple[str, str, str]:
    """
    Process a YouTube video and generate summary.
    
    Args:
        url: YouTube video URL
        api_key: Optional Groq API key (falls back to env variable)
        language: Transcript language
        progress: Gradio progress tracker
        
    Returns:
        Tuple of (summary, video_info, status_message)
    """
    if not url or not url.strip():
        return "", "", "⚠️ Please enter a YouTube URL"
    
    # Validate URL
    extractor = YouTubeExtractor()
    video_id = extractor.extract_video_id(url)
    
    if not video_id:
        return "", "", "❌ Invalid YouTube URL. Please check and try again."
    
    try:
        # Step 1: Extract transcript (20%)
        progress(0.1, desc="📥 Extracting transcript...")
        
        transcript_result = extract_transcript(url, language)
        
        if not transcript_result['success']:
            return "", "", f"❌ Failed to extract transcript: {transcript_result['error']}"
        
        metadata = transcript_result['metadata']
        video_title = metadata.get('title', f'Video {video_id}')
        
        # Step 2: Get video info (30%)
        progress(0.3, desc="📋 Processing video information...")
        
        video_info = f"""### 📹 Video Information
        
**Title:** {video_title}

**Video ID:** {video_id}

**Language:** {metadata.get('language', 'en')}

**Transcript Length:** {metadata.get('transcript_length', 'N/A'):,} characters

**Video Duration:** {metadata.get('video_duration_seconds', 'N/A')}
"""
        
        # Step 3: Generate summary (50-90%)
        progress(0.5, desc="🤖 Generating AI summary...")
        
        # Use provided API key or fall back to environment
        effective_api_key = api_key.strip() if api_key and api_key.strip() else None
        
        summarizer = create_summarizer(
            api_key=effective_api_key,
            model=None
        )
        
        result = summarizer.summarize(
            url=url,
            language=language,
            save_output=False,  # Don't save files in Gradio
            verbose=False
        )
        
        if not result['success']:
            error_msg = result.get('error', 'Unknown error')
            if 'rate limit' in error_msg.lower() or 'quota' in error_msg.lower():
                return "", video_info, f"⏳ API rate limit reached. Please try with your own API key or wait a moment.\n\nError: {error_msg}"
            return "", video_info, f"❌ Failed to generate summary: {error_msg}"
        
        # Step 4: Complete (100%)
        progress(1.0, desc="✅ Complete!")
        
        summary = result['summary']
        usage = result.get('metadata', {}).get('usage', {})
        
        status = f"""✅ **Summary Generated Successfully!**

📊 **Usage Statistics:**
- Tokens Used: {usage.get('total_tokens', 'N/A'):,}
- Estimated Cost: ${usage.get('estimated_cost_usd', 0):.4f}
- Model: {result.get('metadata', {}).get('model', 'N/A')}
"""
        
        return summary, video_info, status
        
    except Exception as e:
        error_str = str(e)
        if 'api_key' in error_str.lower() or 'unauthorized' in error_str.lower():
            return "", "", f"🔑 **API Key Error:** Please provide a valid Groq API key.\n\nDetails: {error_str}"
        return "", "", f"❌ **Error:** {error_str}"


def create_app():
    """Create and configure the Gradio app."""
    
    # Header
    with gr.Blocks() as app:
        # Custom header
        gr.HTML("""
        <div class="app-header">
            <h1>📚 YouTube to Book Summary</h1>
            <p>Transform any YouTube video into a comprehensive, book-style summary using AI</p>
        </div>
        """)
        
        # Main content
        with gr.Row():
            with gr.Column(scale=2):
                # Input section
                with gr.Group():
                    gr.Markdown("### 🎬 Video Input")
                    
                    url_input = gr.Textbox(
                        label="YouTube URL",
                        placeholder="https://www.youtube.com/watch?v=...",
                        lines=1,
                        max_lines=1,
                        show_label=True
                    )
                    
                    with gr.Accordion("⚙️ Advanced Settings", open=False):
                        api_key_input = gr.Textbox(
                            label="Groq API Key (Optional)",
                            placeholder="Leave empty to use default key",
                            type="password",
                            lines=1
                        )
                        
                        language_input = gr.Dropdown(
                            label="Transcript Language",
                            choices=["en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh"],
                            value="en",
                            interactive=True
                        )
                        
                        gr.Markdown("""
                        💡 **Tip:** If the default API key is rate-limited, you can:
                        1. Get a free API key from [console.groq.com](https://console.groq.com/)
                        2. Paste it above to continue using the app
                        """)
                    
                    generate_btn = gr.Button(
                        "🚀 Generate Summary",
                        variant="primary",
                        elem_classes=["primary-btn"]
                    )
                
                # Status output
                status_output = gr.Markdown(
                    label="Status",
                    elem_classes=["status-info"]
                )
                
                # Video info
                video_info_output = gr.Markdown(
                    label="Video Information",
                    visible=True
                )
            
            with gr.Column(scale=3):
                # Summary output
                summary_output = gr.Markdown(
                    label="Generated Summary",
                    elem_classes=["markdown-text"],
                    show_label=True
                )
        
        # Examples
        gr.Examples(
            examples=[
                ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
                ["https://www.youtube.com/watch?v=jNQXAC9IVRw"],
                ["https://youtu.be/aircAruvnKk"],
            ],
            inputs=[url_input],
            label="📝 Example Videos (Try these!)"
        )
        
        # Footer
        gr.HTML("""
        <div class="footer">
            <p>Powered by <strong>Groq LLM</strong> | Built with ❤️ using Gradio</p>
            <p>Transform YouTube videos into comprehensive book-style summaries</p>
        </div>
        """)
        
        # Event handlers
        generate_btn.click(
            fn=process_video,
            inputs=[url_input, api_key_input, language_input],
            outputs=[summary_output, video_info_output, status_output],
            api_name="generate"
        )
        
        # Also allow Enter key to submit
        url_input.submit(
            fn=process_video,
            inputs=[url_input, api_key_input, language_input],
            outputs=[summary_output, video_info_output, status_output]
        )
    
    return app


# Create the app
app = create_app()


if __name__ == "__main__":
    # For local development
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        css=CUSTOM_CSS,
        theme=gr.themes.Soft()
    )
