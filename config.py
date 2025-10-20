"""
AI Benchmark - LLM Model Benchmarking Application
Supports ChatGPT, Gemini, Claude, Grok, and local models (LLaMA, Qwen, Gemma)
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ModelConfig(BaseModel):
    """Configuration for a model"""
    name: str
    provider: str  # openai, anthropic, google, xai, local
    model_id: str
    enabled: bool = True
    params: Dict[str, Any] = {}


class BenchmarkTest(BaseModel):
    """Configuration for a benchmark test"""
    name: str
    description: str
    prompt: str
    category: str = "general"
    expected_keywords: List[str] = []
    max_tokens: int = 500


class BenchmarkResult(BaseModel):
    """Result of a benchmark test"""
    model_name: str
    test_name: str
    prompt: str
    response: str
    latency: float  # in seconds
    tokens_used: Optional[int] = None
    success: bool = True
    error: Optional[str] = None


# Default benchmark tests
DEFAULT_TESTS = [
    BenchmarkTest(
        name="Code Generation",
        description="Test ability to generate Python code",
        prompt="Write a Python function to calculate the factorial of a number using recursion.",
        category="coding",
        expected_keywords=["def", "factorial", "return", "if"],
        max_tokens=300
    ),
    BenchmarkTest(
        name="Creative Writing",
        description="Test creative writing abilities",
        prompt="Write a short story (3-4 sentences) about a robot learning to paint.",
        category="creative",
        expected_keywords=["robot", "paint"],
        max_tokens=200
    ),
    BenchmarkTest(
        name="Logical Reasoning",
        description="Test logical reasoning capabilities",
        prompt="If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly? Explain your reasoning.",
        category="reasoning",
        expected_keywords=["logic", "conclusion", "reasoning"],
        max_tokens=300
    ),
    BenchmarkTest(
        name="Math Problem",
        description="Test mathematical problem-solving",
        prompt="A train travels 120 miles in 2 hours. If it maintains the same speed, how far will it travel in 5 hours? Show your work.",
        category="math",
        expected_keywords=["speed", "distance", "300"],
        max_tokens=200
    ),
    BenchmarkTest(
        name="Summarization",
        description="Test text summarization ability",
        prompt="Summarize the following in one sentence: The Industrial Revolution was a period of major industrialization and innovation during the late 1700s and early 1800s. It began in Great Britain and quickly spread throughout the world.",
        category="summarization",
        expected_keywords=["Industrial Revolution", "1700s", "Britain"],
        max_tokens=100
    ),
]
