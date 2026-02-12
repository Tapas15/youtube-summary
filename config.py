"""Configuration management for YouTube to Book Summary."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the application."""
    
    # Groq API Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Output Settings
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "./summaries"))
    
    # Transcript Settings
    MAX_TRANSCRIPT_LENGTH: int = 25000  # Max characters per API call
    CHUNK_OVERLAP: int = 500  # Overlap between chunks
    
    # Summary Settings
    SUMMARY_LANGUAGE: str = "English"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set. Please add it to your .env file.")
        return True
    
    @classmethod
    def ensure_output_dir(cls) -> Path:
        """Ensure output directory exists."""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        return cls.OUTPUT_DIR


# Instance for import
config = Config()
