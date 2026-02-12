"""YouTube transcript extraction module."""
import re
import urllib.request
import json
from typing import Optional, Dict, Any, List
from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeExtractor:
    """Extract transcripts from YouTube videos."""
    
    def get_video_title(self, video_id: str) -> str:
        """
        Fetch the video title from YouTube using oEmbed.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video title or fallback title if not available
        """
        try:
            # Use YouTube's oEmbed API to get video info
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            
            with urllib.request.urlopen(oembed_url, timeout=10) as response:
                data = json.loads(response.read().decode())
                return data.get('title', f"YouTube Video {video_id}")
        except Exception:
            # Fallback to generic title if oEmbed fails
            return f"YouTube Video {video_id}"
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
            r'(?:youtube\.com/shorts/)([0-9A-Za-z_-]{11})',
            r'(?:youtube\.com/embed/)([0-9A-Za-z_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_transcript(self, url: str, language: str = "en") -> Dict[str, Any]:
        """
        Get transcript from a YouTube video.
        
        Args:
            url: YouTube video URL
            language: Preferred language code (default: "en")
            
        Returns:
            Dict containing transcript text and metadata
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")
        
        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            
            # Try to find transcript in preferred language
            transcript = None
            detected_language = language
            
            try:
                transcript = transcript_list.find_manually_created_transcript([language])
            except Exception:
                pass
            
            if not transcript:
                try:
                    transcript = transcript_list.find_generated_transcript([language])
                except Exception:
                    pass
            
            if not transcript:
                all_transcripts = list(transcript_list)
                if all_transcripts:
                    transcript = all_transcripts[0]
                else:
                    raise ValueError(f"No transcripts available for video: {url}")
            
            # Get detected language
            if hasattr(transcript, 'language_code'):
                detected_language = transcript.language_code
            
            # Fetch the transcript data
            transcript_data = transcript.fetch()
            
            # Combine into continuous text and calculate duration
            text_parts = []
            total_duration = 0.0
            
            for entry in transcript_data:
                # entry is a FetchedTranscriptSnippet dataclass, not a dict
                text = entry.text if hasattr(entry, 'text') else str(entry)
                # Clean up timestamp markers
                if '[' in text and ']' in text:
                    text = re.sub(r'\[.*?\]', '', text).strip()
                text_parts.append(text)
                
                # Calculate video duration from transcript entries
                if hasattr(entry, 'start') and hasattr(entry, 'duration'):
                    end_time = entry.start + entry.duration
                    if end_time > total_duration:
                        total_duration = end_time
            
            full_text = ' '.join(text_parts)
            
            # Fetch the actual video title
            video_title = self.get_video_title(video_id)
            
            metadata = {
                'video_id': video_id,
                'language': detected_language,
                'title': video_title,
                'transcript_length': len(full_text),
                'video_duration_seconds': total_duration if total_duration > 0 else None,
            }
            
            return {
                'success': True,
                'text': full_text,
                'metadata': metadata
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': None,
                'metadata': {'video_id': video_id}
            }
    
    def get_transcript_with_timestamps(self, url: str, language: str = "en") -> Dict[str, Any]:
        """
        Get transcript with timestamps from a YouTube video.
        
        Args:
            url: YouTube video URL
            language: Preferred language code (default: "en")
            
        Returns:
            Dict containing transcript entries with timestamps
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")
        
        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            
            # Try to find transcript in preferred language
            transcript = None
            
            try:
                transcript = transcript_list.find_manually_created_transcript([language])
            except Exception:
                pass
            
            if not transcript:
                try:
                    transcript = transcript_list.find_generated_transcript([language])
                except Exception:
                    pass
            
            if not transcript:
                all_transcripts = list(transcript_list)
                if all_transcripts:
                    transcript = all_transcripts[0]
                else:
                    raise ValueError(f"No transcripts available for video: {url}")
            
            # Fetch the transcript data
            transcript_data = transcript.fetch()
            
            # Build timestamped entries
            entries = []
            for entry in transcript_data:
                text = entry.text if hasattr(entry, 'text') else str(entry)
                start = entry.start if hasattr(entry, 'start') else 0
                duration = entry.duration if hasattr(entry, 'duration') else 0
                
                # Clean up timestamp markers in text
                if '[' in text and ']' in text:
                    text = re.sub(r'\[.*?\]', '', text).strip()
                
                entries.append({
                    'text': text,
                    'start': start,
                    'duration': duration,
                    'timestamp': self._format_timestamp(start),
                })
            
            # Fetch the actual video title
            video_title = self.get_video_title(video_id)
            
            return {
                'success': True,
                'entries': entries,
                'metadata': {
                    'video_id': video_id,
                    'language': language,
                    'title': video_title,
                    'total_entries': len(entries),
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'entries': [],
                'metadata': {'video_id': video_id}
            }
    
    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """Format seconds to HH:MM:SS or MM:SS format."""
        seconds = int(seconds)
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def chunk_transcript(self, text: str, max_length: int = 25000, overlap: int = 500) -> list:
        """Split transcript into manageable chunks."""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + max_length
            
            if end < len(text):
                for i in range(end, max(end - 500, start), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunks.append(text[start:end])
            start = end - overlap
            
            if start >= len(text):
                break
        
        return chunks


def extract_transcript(url: str, language: str = "en") -> Dict[str, Any]:
    """Convenience function to extract transcript from URL."""
    extractor = YouTubeExtractor()
    return extractor.get_transcript(url, language)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        result = extract_transcript(url)
        
        if result['success']:
            print(f"Transcript extracted: {result['metadata']['transcript_length']} chars")
            print(f"\nFirst 500 chars:\n{result['text'][:500]}...")
        else:
            print(f"Error: {result['error']}")
    else:
        print("Usage: python youtube_transcript.py <YouTube_URL>")
