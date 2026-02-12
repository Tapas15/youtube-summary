"""Transcript statistics calculator module."""
from typing import Dict, Any
from datetime import timedelta


class TranscriptStatistics:
    """Calculate and manage transcript statistics."""
    
    # Average reading speed (words per minute)
    READING_SPEED_WPM = 200
    
    @classmethod
    def calculate(cls, text: str, video_duration_seconds: float = None) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics for a transcript.
        
        Args:
            text: The transcript text
            video_duration_seconds: Optional video duration in seconds
            
        Returns:
            Dictionary containing all statistics
        """
        if not text:
            return cls._empty_stats()
        
        # Basic counts
        word_count = cls._count_words(text)
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        paragraph_count = cls._count_paragraphs(text)
        sentence_count = cls._count_sentences(text)
        
        # Time calculations
        reading_time_minutes = cls._calculate_reading_time(word_count)
        
        # Speaking rate (if video duration provided)
        speaking_rate = None
        if video_duration_seconds and video_duration_seconds > 0:
            speaking_rate = cls._calculate_speaking_rate(
                word_count, 
                video_duration_seconds
            )
        
        return {
            'word_count': word_count,
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'paragraph_count': paragraph_count,
            'sentence_count': sentence_count,
            'reading_time_minutes': reading_time_minutes,
            'reading_time_formatted': cls._format_time(reading_time_minutes),
            'video_duration_seconds': video_duration_seconds,
            'video_duration_formatted': cls._format_duration(video_duration_seconds) if video_duration_seconds else None,
            'speaking_rate_wpm': speaking_rate,
            'average_word_length': cls._average_word_length(text, word_count),
            'average_sentence_length': round(word_count / sentence_count, 1) if sentence_count > 0 else 0,
        }
    
    @staticmethod
    def _count_words(text: str) -> int:
        """Count words in text."""
        # Split by whitespace and filter empty strings
        words = [w for w in text.split() if w]
        return len(words)
    
    @staticmethod
    def _count_paragraphs(text: str) -> int:
        """Count paragraphs (separated by double newlines)."""
        if not text.strip():
            return 0
        # Split by double newlines and filter empty
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        return max(1, len(paragraphs))
    
    @staticmethod
    def _count_sentences(text: str) -> int:
        """Count sentences (ending with . ! ?)."""
        import re
        # Match sentence endings
        sentences = re.split(r'[.!?]+', text)
        # Filter out empty strings
        sentences = [s for s in sentences if s.strip()]
        return max(1, len(sentences))
    
    @classmethod
    def _calculate_reading_time(cls, word_count: int) -> float:
        """Calculate reading time in minutes."""
        return round(word_count / cls.READING_SPEED_WPM, 1)
    
    @classmethod
    def _calculate_speaking_rate(cls, word_count: int, duration_seconds: float) -> int:
        """Calculate speaking rate in words per minute."""
        if duration_seconds <= 0:
            return 0
        duration_minutes = duration_seconds / 60
        return round(word_count / duration_minutes)
    
    @staticmethod
    def _format_time(minutes: float) -> str:
        """Format time in minutes to human-readable string."""
        if minutes < 1:
            seconds = int(minutes * 60)
            return f"{seconds} seconds"
        elif minutes < 60:
            return f"{minutes:.1f} minutes"
        else:
            hours = int(minutes // 60)
            remaining_minutes = int(minutes % 60)
            return f"{hours}h {remaining_minutes}m"
    
    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration in seconds to HH:MM:SS format."""
        if seconds is None:
            return "N/A"
        
        td = timedelta(seconds=int(seconds))
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def _average_word_length(text: str, word_count: int) -> float:
        """Calculate average word length."""
        if word_count == 0:
            return 0
        # Remove punctuation for accurate measurement
        import re
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return 0
        total_chars = sum(len(w) for w in words)
        return round(total_chars / len(words), 1)
    
    @staticmethod
    def _empty_stats() -> Dict[str, Any]:
        """Return empty statistics dictionary."""
        return {
            'word_count': 0,
            'character_count': 0,
            'character_count_no_spaces': 0,
            'paragraph_count': 0,
            'sentence_count': 0,
            'reading_time_minutes': 0,
            'reading_time_formatted': '0 seconds',
            'video_duration_seconds': None,
            'video_duration_formatted': None,
            'speaking_rate_wpm': None,
            'average_word_length': 0,
            'average_sentence_length': 0,
        }


def calculate_transcript_stats(text: str, video_duration_seconds: float = None) -> Dict[str, Any]:
    """Convenience function to calculate transcript statistics."""
    return TranscriptStatistics.calculate(text, video_duration_seconds)


if __name__ == "__main__":
    # Test the statistics calculator
    sample_text = """
    Welcome everyone to this video. Today we are going to discuss the importance of 
    artificial intelligence in modern software development.
    
    AI has become an integral part of our daily lives. From voice assistants to 
    recommendation systems, we interact with AI on a regular basis.
    
    In this video, we will explore how developers can leverage AI tools to improve 
    their productivity and create better software solutions.
    """
    
    stats = calculate_transcript_stats(sample_text, video_duration_seconds=180)
    
    print("Transcript Statistics:")
    print(f"  Word Count: {stats['word_count']}")
    print(f"  Character Count: {stats['character_count']}")
    print(f"  Reading Time: {stats['reading_time_formatted']}")
    print(f"  Video Duration: {stats['video_duration_formatted']}")
    print(f"  Speaking Rate: {stats['speaking_rate_wpm']} WPM")
    print(f"  Paragraphs: {stats['paragraph_count']}")
    print(f"  Sentences: {stats['sentence_count']}")
