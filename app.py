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


# Create the Gradio interface
with gr.Blocks(title="YouTube to Book Summary") as app:
    
    # Header
    gr.Markdown("""
    # 📚 YouTube to Book Summary Converter
    
    Transform any YouTube video into a comprehensive, book-style summary using AI (Groq LLM).
    """)
    
    # Main content
    with gr.Row():
        with gr.Column(scale=2):
            # Input section
            gr.Markdown("### 🎬 Video Input")
            
            url_input = gr.Textbox(
                label="YouTube URL",
                placeholder="https://www.youtube.com/watch?v=...",
                lines=1,
                max_lines=1
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
                variant="primary"
            )
            
            # Status output
            status_output = gr.Markdown(
                label="Status"
            )
            
            # Video info
            video_info_output = gr.Markdown(
                label="Video Information"
            )
        
        with gr.Column(scale=3):
            # Summary output
            summary_output = gr.Markdown(
                label="Generated Summary"
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
    gr.Markdown("""
    ---
    **Powered by Groq LLM** | Built with ❤️ using Gradio
    
    Transform YouTube videos into comprehensive book-style summaries
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


if __name__ == "__main__":
    # For local development
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(
            primary_hue="purple",
            secondary_hue="blue",
            neutral_hue="slate",
        )
    )
