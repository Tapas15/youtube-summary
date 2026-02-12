"""Groq API client for LLM processing."""
import os
from typing import Optional, List, Dict, Any
from groq import Groq, RateLimitError, APIError
from config import config


class GroqClient:
    """Client for interacting with Groq API."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Groq client.
        
        Args:
            api_key: Groq API key (defaults to config)
            model: Model name (defaults to config)
        """
        self.api_key = api_key or config.GROQ_API_KEY
        self.model = model or config.GROQ_MODEL
        self.client = Groq(api_key=self.api_key)
        
        # Model pricing (approximate, per million tokens)
        self.pricing = {
            "llama-3.3-70b-versatile": {"input": 0.59, "output": 1.99},
            "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
            "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
            "gemma2-9b-it": {"input": 0.14, "output": 0.14},
        }
    
    def count_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        # Average: 4 characters per token
        return len(text) // 4
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for API call."""
        pricing = self.pricing.get(self.model, {"input": 0.5, "output": 1.0})
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 8000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to Groq.
        
        Args:
            messages: List of message dictionaries
            max_tokens: Maximum output tokens
            temperature: Sampling temperature
            system_prompt: Optional system prompt
            
        Returns:
            API response dictionary
        """
        # Add system prompt if provided
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = self.estimate_cost(input_tokens, output_tokens)
            
            return {
                'success': True,
                'content': response.choices[0].message.content,
                'usage': {
                    'prompt_tokens': input_tokens,
                    'completion_tokens': output_tokens,
                    'total_tokens': input_tokens + output_tokens,
                    'estimated_cost_usd': cost
                },
                'model': self.model
            }
            
        except RateLimitError as e:
            return {
                'success': False,
                'error': f"Rate limit exceeded: {str(e)}",
                'error_type': 'rate_limit'
            }
        except APIError as e:
            return {
                'success': False,
                'error': f"API error: {str(e)}",
                'error_type': 'api_error'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'error_type': 'unknown'
            }
    
    def summarize_transcript(
        self,
        transcript: str,
        prompt_template: str,
        chunk_summaries: Optional[List[str]] = None,
        max_tokens: int = 12000,
        temperature: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive summary from transcript.
        
        Args:
            transcript: Full transcript text
            prompt_template: The prompt template from youtube_summary.md
            chunk_summaries: Optional pre-processed chunk summaries
            max_tokens: Maximum output tokens
            temperature: Sampling temperature
            
        Returns:
            Summary result dictionary
        """
        # Handle chunked transcripts
        if chunk_summaries:
            # Combine chunk summaries into an intermediate summary
            combined_summary = "\n\n".join(chunk_summaries)
            user_message = f"""Based on these chapter-by-chapter summaries, create a comprehensive book-style summary following the format below:

{combined_summary}

---
{PROMPT_SUFFIX}
"""
        else:
            user_message = f"""{transcript}

---
{PROMPT_SUFFIX}
"""
        
        messages = [
            {"role": "user", "content": user_message}
        ]
        
        response = self.chat_completion(
            messages=messages,
            system_prompt=prompt_template,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        return response


# Prompt suffix used in summarize_transcript
PROMPT_SUFFIX = """Using the above content, create a comprehensive book-style summary following the youtube_summary.md template exactly. Include:
- Executive Overview (2-3 paragraphs)
- Introduction with background and presenter context
- Chapter-by-Chapter Summary with detailed analysis
- Key Concepts and Definitions
- Key Takeaways (numbered)
- Memorable Quotations (3-5 quotes)
- Practical Applications
- Critical Analysis
- Further Reading/Sources
- Conclusion

Write in flowing prose, avoid excessive lists, and maximize depth and value."""


def create_client(api_key: Optional[str] = None, model: Optional[str] = None) -> GroqClient:
    """Factory function to create Groq client."""
    return GroqClient(api_key=api_key, model=model)


if __name__ == "__main__":
    # Test the client
    client = create_client()
    
    if not config.GROQ_API_KEY:
        print("Warning: GROQ_API_KEY not set. Set it in .env file.")
    else:
        print(f"✓ Groq client initialized with model: {client.model}")
        print(f"  Available models: {list(client.pricing.keys())}")
