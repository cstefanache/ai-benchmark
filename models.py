"""
Model adapters for different LLM providers
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import time
import os


class ModelAdapter(ABC):
    """Base class for model adapters"""
    
    def __init__(self, model_id: str, params: Dict[str, Any] = None):
        self.model_id = model_id
        self.params = params or {}
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 500) -> tuple[str, float, Optional[int]]:
        """
        Generate a response to the prompt
        Returns: (response_text, latency_seconds, tokens_used)
        """
        pass


class OpenAIAdapter(ModelAdapter):
    """Adapter for OpenAI models (ChatGPT)"""
    
    def __init__(self, model_id: str = "gpt-3.5-turbo", params: Dict[str, Any] = None):
        super().__init__(model_id, params)
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate(self, prompt: str, max_tokens: int = 500) -> tuple[str, float, Optional[int]]:
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                **self.params
            )
            latency = time.time() - start_time
            tokens = response.usage.total_tokens if response.usage else None
            return response.choices[0].message.content, latency, tokens
        except Exception as e:
            latency = time.time() - start_time
            raise Exception(f"OpenAI API error: {str(e)}")


class AnthropicAdapter(ModelAdapter):
    """Adapter for Anthropic models (Claude)"""
    
    def __init__(self, model_id: str = "claude-3-sonnet-20240229", params: Dict[str, Any] = None):
        super().__init__(model_id, params)
        from anthropic import Anthropic
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def generate(self, prompt: str, max_tokens: int = 500) -> tuple[str, float, Optional[int]]:
        start_time = time.time()
        try:
            response = self.client.messages.create(
                model=self.model_id,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
                **self.params
            )
            latency = time.time() - start_time
            tokens = response.usage.input_tokens + response.usage.output_tokens if response.usage else None
            return response.content[0].text, latency, tokens
        except Exception as e:
            latency = time.time() - start_time
            raise Exception(f"Anthropic API error: {str(e)}")


class GoogleAdapter(ModelAdapter):
    """Adapter for Google models (Gemini)"""
    
    def __init__(self, model_id: str = "gemini-pro", params: Dict[str, Any] = None):
        super().__init__(model_id, params)
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model_id)
    
    def generate(self, prompt: str, max_tokens: int = 500) -> tuple[str, float, Optional[int]]:
        start_time = time.time()
        try:
            generation_config = {
                "max_output_tokens": max_tokens,
                **self.params
            }
            response = self.model.generate_content(prompt, generation_config=generation_config)
            latency = time.time() - start_time
            return response.text, latency, None
        except Exception as e:
            latency = time.time() - start_time
            raise Exception(f"Google API error: {str(e)}")


class XAIAdapter(ModelAdapter):
    """Adapter for xAI models (Grok)"""
    
    def __init__(self, model_id: str = "grok-beta", params: Dict[str, Any] = None):
        super().__init__(model_id, params)
        from openai import OpenAI
        # Grok uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
    
    def generate(self, prompt: str, max_tokens: int = 500) -> tuple[str, float, Optional[int]]:
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                **self.params
            )
            latency = time.time() - start_time
            tokens = response.usage.total_tokens if response.usage else None
            return response.choices[0].message.content, latency, tokens
        except Exception as e:
            latency = time.time() - start_time
            raise Exception(f"xAI API error: {str(e)}")


class LocalLlamaAdapter(ModelAdapter):
    """Adapter for local models using llama.cpp"""
    
    def __init__(self, model_path: str, params: Dict[str, Any] = None):
        super().__init__(model_path, params)
        from llama_cpp import Llama
        
        # Default parameters for local models
        default_params = {
            "n_ctx": 2048,
            "n_threads": 4,
            "n_gpu_layers": 0,  # Set to >0 if you have GPU support
        }
        default_params.update(self.params)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        self.llm = Llama(model_path=model_path, **default_params)
    
    def generate(self, prompt: str, max_tokens: int = 500) -> tuple[str, float, Optional[int]]:
        start_time = time.time()
        try:
            response = self.llm(
                prompt,
                max_tokens=max_tokens,
                echo=False,
                **{k: v for k, v in self.params.items() if k not in ["n_ctx", "n_threads", "n_gpu_layers"]}
            )
            latency = time.time() - start_time
            tokens = response.get("usage", {}).get("total_tokens")
            return response["choices"][0]["text"], latency, tokens
        except Exception as e:
            latency = time.time() - start_time
            raise Exception(f"Local model error: {str(e)}")
