#!/usr/bin/env python3
"""
YouTube to Book Summary Converter

A CLI tool that extracts transcripts from YouTube videos and generates
comprehensive book-style summaries using Groq's LLM API.

Usage:
    python main.py <YouTube_URL> [--lang <language>] [--save/--no-save] [--verbose]
    python main.py --interactive
    python main.py --batch <file_with_urls.txt>

Requirements:
    - GROQ_API_KEY in .env file
    - python-youtube-transcript-api
    - groq SDK
"""
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

from config import config
from summarizer import YouTubeBookSummarizer, create_summarizer


def print_banner():
    """Print application banner."""
    banner = """
================================================================
                                                             
     YouTube to Book Summary Converter                        
                                                             
     Transform YouTube videos into comprehensive book-style   
     summaries using AI (Groq LLM)                           
                                                             
================================================================
"""
    print(banner)


def check_api_key():
    """Check if API key is configured."""
    if not config.GROQ_API_KEY:
        print("[ERROR] GROQ_API_KEY not found!")
        print("\nPlease set up your environment:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Groq API key to .env")
        print("  3. Get your API key from: https://console.groq.com/")
        return False
    return True


def process_single_video(url: str, args: argparse.Namespace):
    """Process a single YouTube video."""
    print(f"\n[*] Processing: {url}")
    print("-" * 60)
    
    # Create summarizer
    summarizer = create_summarizer(
        api_key=config.GROQ_API_KEY,
        model=args.model,
    )
    
    # Generate summary
    result = summarizer.summarize(
        url=url,
        language=args.lang,
        save_output=not args.no_save,
        verbose=args.verbose,
    )
    
    if result.get('success'):
        # Always print summary preview when successful
        metadata = result.get('metadata', {})
        
        if not args.no_save:
            output_files = metadata.get('output_file', 'N/A')
            if isinstance(output_files, tuple):
                book_path, pdf_path, transcript_path = output_files
                import os
                abs_path = os.path.abspath(book_path)
                print(f"\n{'='*60}")
                print("[FILES] SAVED IN: " + os.path.dirname(abs_path))
                print(f"{'='*60}")
                print(f"  [BOOK-WORD] {os.path.basename(book_path)}")
                print(f"  [BOOK-PDF]  {os.path.basename(pdf_path)}")
                print(f"  [TRANSCRIPT] {os.path.basename(transcript_path)}")
                print(f"\nFull path: {os.path.dirname(abs_path)}")
            else:
                print(f"\n[OUTPUT] saved to: {output_files}")
        
        # Always show summary
        print(f"\n{'='*60}")
        print("GENERATED SUMMARY:")
        print(f"{'='*60}\n")
        print(result.get('summary', 'No summary generated'))
    else:
        print(f"\n[ERROR] Failed to generate summary: {result['error']}")
        return False
    
    return True


def process_batch_file(filepath: str, args: argparse.Namespace):
    """Process multiple videos from a file."""
    path = Path(filepath)
    
    if not path.exists():
        print(f"[ERROR] File not found: {filepath}")
        return
    
    urls = path.read_text().strip().split('\n')
    urls = [u.strip() for u in urls if u.strip() and not u.startswith('#')]
    
    print(f"\n[BATCH] Mode: {len(urls)} videos to process")
    
    # Create summarizer once
    summarizer = create_summarizer(
        api_key=config.GROQ_API_KEY,
        model=args.model,
    )
    
    success_count = 0
    failed_count = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n{'-'*60}")
        print(f"[{i}/{len(urls)}] Processing: {url}")
        
        result = summarizer.summarize(
            url=url,
            language=args.lang,
            save_output=not args.no_save,
            verbose=args.verbose,
        )
        
        if result['success']:
            success_count += 1
            if not args.verbose:
                print(f"  [OK] Success")
        else:
            failed_count += 1
            print(f"  [FAIL] Error: {result['error']}")
    
    print(f"\n{'='*60}")
    print(f"[BATCH COMPLETE] {success_count} succeeded, {failed_count} failed")


def interactive_mode():
    """Interactive mode for entering URLs."""
    print("\n[INTERACTIVE MODE]")
    print("Enter YouTube URLs (one per line).")
    print("Press Enter on empty line to start processing.\n")
    
    urls = []
    while True:
        try:
            url = input("  YouTube URL: ").strip()
            if not url:
                if urls:
                    break
                else:
                    print("  Please enter at least one URL")
                    continue
            urls.append(url)
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
    
    if urls:
        print(f"\nProcessing {len(urls)} video(s)...\n")
        for url in urls:
            process_single_video(url, argparse.Namespace(
                lang='en',
                model=None,
                no_save=False,
                verbose=True,
            ))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert YouTube videos to book-style summaries using Groq AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/watch?v=..." --verbose
  %(prog)s "https://www.youtube.com/watch?v=..." --lang es
  %(prog)s --batch urls.txt
  %(prog)s --interactive

Get Groq API key: https://console.groq.com/
        """,
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='YouTube video URL',
    )
    
    parser.add_argument(
        '--lang', '-l',
        default='en',
        help='Transcript language (default: en)',
    )
    
    parser.add_argument(
        '--model', '-m',
        help='Groq model to use (default: llama-3.3-70b-versatile)',
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help="Don't save output to file",
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress',
    )
    
    parser.add_argument(
        '--batch', '-b',
        help='Process URLs from a file (one per line)',
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Enter interactive mode',
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Validate API key
    if not check_api_key():
        sys.exit(1)
    
    # Ensure output directory exists
    config.ensure_output_dir()
    
    # Process based on mode
    if args.interactive:
        interactive_mode()
    elif args.batch:
        process_batch_file(args.batch, args)
    elif args.url:
        process_single_video(args.url, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
