import os
import tiktoken
from datetime import datetime
from typing import Dict, Any, Optional

class TokenLogger:
    """Comprehensive token usage and cost tracking for all LLM activities."""
    
    # OpenAI pricing per 1K tokens (as of 2024, update as needed)
    PRICING = {
        "gpt-4o": {"input": 0.005, "output": 0.015},      # $5.00 / 1M input, $15.00 / 1M output
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006}, # $0.15 / 1M input, $0.60 / 1M output
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},   # $10.00 / 1M input, $30.00 / 1M output
        "gpt-4": {"input": 0.03, "output": 0.06},         # $30.00 / 1M input, $60.00 / 1M output
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}, # $0.50 / 1M input, $1.50 / 1M output
        "gpt-4.1-nano": {"input": 0.0001, "output": 0.0002},  # Estimated for nano model
        "text-embedding-3-large": {"input": 0.00013, "output": 0.0}, # $0.13 / 1M tokens (embedding only)
    }
    
    def __init__(self, log_file: str = "shared/logs/token_usage.log"):
        """Initialize the token logger."""
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    def count_tokens(self, text: str, model: str = "gpt-4") -> int:
        """Count tokens in text using the appropriate tokenizer for the model."""
        try:
            if model.startswith("text-embedding"):
                encoding = tiktoken.get_encoding("cl100k_base")
            else:
                encoding = tiktoken.encoding_for_model(model)
        except Exception:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        return len(encoding.encode(text))
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost based on input and output tokens for the specific model."""
        model_pricing = self.PRICING.get(model, self.PRICING["gpt-4.1-nano"])
        
        input_cost = (input_tokens / 1000) * model_pricing["input"]
        output_cost = (output_tokens / 1000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    def log_activity(self, activity_type: str, model: str, input_tokens: int, 
                    output_tokens: int = 0, additional_info: Optional[Dict[str, Any]] = None):
        """Log token usage and cost for any LLM activity."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_tokens = input_tokens + output_tokens
        cost = self.calculate_cost(input_tokens, output_tokens, model)
        
        log_entry = f"[{timestamp}] {activity_type.upper()}\n"
        log_entry += f"Model: {model}\n"
        log_entry += f"Input tokens: {input_tokens:,}\n"
        log_entry += f"Output tokens: {output_tokens:,}\n"
        log_entry += f"Total tokens: {total_tokens:,}\n"
        log_entry += f"Estimated cost: ${cost:.6f}\n"
        
        if additional_info:
            for key, value in additional_info.items():
                log_entry += f"{key}: {value}\n"
        
        log_entry += "-" * 50 + "\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[TOKEN LOGGING ERROR] Could not write to {self.log_file}: {e}")
    
    def log_embedding(self, text: str, model: str = "text-embedding-3-large", 
                     file_name: Optional[str] = None):
        """Log embedding token usage."""
        input_tokens = self.count_tokens(text, model)
        additional_info = {"File": file_name} if file_name else None
        self.log_activity("embedding", model, input_tokens, 0, additional_info)
    
    def log_answer_generation(self, prompt: str, response: str, model: str = "gpt-4.1-nano",
                            query: Optional[str] = None):
        """Log answer generation token usage."""
        input_tokens = self.count_tokens(prompt, model)
        output_tokens = self.count_tokens(response, model)
        additional_info = {"Query": query} if query else None
        self.log_activity("answer_generation", model, input_tokens, output_tokens, additional_info)
    
    def log_summarization(self, input_text: str, summary: str, model: str = "gpt-4.1-nano",
                         summary_type: str = "document"):
        """Log summarization token usage."""
        input_tokens = self.count_tokens(input_text, model)
        output_tokens = self.count_tokens(summary, model)
        additional_info = {"Summary type": summary_type}
        self.log_activity("summarization", model, input_tokens, output_tokens, additional_info)
    
    def log_chat_summarization(self, chat_history: str, summary: str, model: str = "gpt-4.1-nano"):
        """Log chat history summarization token usage."""
        input_tokens = self.count_tokens(chat_history, model)
        output_tokens = self.count_tokens(summary, model)
        self.log_activity("chat_summarization", model, input_tokens, output_tokens)
    
    def get_total_usage(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get total token usage and cost for a date range."""
        # This is a placeholder for future implementation
        # Would parse the log file and aggregate usage
        return {
            "total_tokens": 0,
            "total_cost": 0.0,
            "activities": {}
        }

# Global instance for easy access
token_logger = TokenLogger() 