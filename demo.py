"""
Demo script to test the benchmark application without API keys
Uses mock adapters to simulate model responses
"""

import time
from typing import Dict, Any, Optional

from config import ModelConfig, BenchmarkTest, DEFAULT_TESTS
from benchmark import BenchmarkEngine
from models import ModelAdapter


class MockAdapter(ModelAdapter):
    """Mock adapter for testing without API keys"""
    
    def __init__(self, model_id: str, params: Dict[str, Any] = None):
        super().__init__(model_id, params)
        self.delay = params.get("delay", 0.5) if params else 0.5
    
    def generate(self, prompt: str, max_tokens: int = 500) -> tuple[str, float, Optional[int]]:
        """Generate a mock response"""
        time.sleep(self.delay)
        
        # Generate a simple mock response based on the prompt
        response = f"This is a mock response to: '{prompt[:50]}...'\n\n"
        response += "In a real scenario, this would be the model's actual response. "
        response += "The mock adapter simulates the API call with a delay and returns this test response."
        
        latency = self.delay
        tokens = len(prompt.split()) + len(response.split())
        
        return response, latency, tokens


def test_benchmark_engine():
    """Test the benchmark engine with mock models"""
    print("=" * 80)
    print("AI Benchmark - Demo Test")
    print("=" * 80)
    print()
    
    # Create engine
    engine = BenchmarkEngine()
    
    # Add mock models
    print("Adding mock models...")
    models = [
        ModelConfig(name="Mock-GPT", provider="openai", model_id="mock-gpt", enabled=True, params={"delay": 0.3}),
        ModelConfig(name="Mock-Claude", provider="anthropic", model_id="mock-claude", enabled=True, params={"delay": 0.4}),
        ModelConfig(name="Mock-Gemini", provider="google", model_id="mock-gemini", enabled=True, params={"delay": 0.5}),
    ]
    
    # Override the add_model method to use MockAdapter
    original_add_model = engine.add_model
    
    def mock_add_model(config: ModelConfig) -> bool:
        if not config.enabled:
            return False
        try:
            adapter = MockAdapter(config.model_id, config.params)
            engine.models[config.name] = adapter
            print(f"  ✓ Added {config.name}")
            return True
        except Exception as e:
            print(f"  ✗ Error adding {config.name}: {str(e)}")
            return False
    
    engine.add_model = mock_add_model
    
    for model in models:
        engine.add_model(model)
    
    print()
    
    # Use first 3 default tests
    tests = DEFAULT_TESTS[:3]
    
    print(f"Running {len(tests)} tests on {len(engine.models)} models...")
    print()
    
    # Run benchmark
    results = engine.run_benchmark(tests, parallel=False)
    
    print(f"Completed {len(results)} test runs")
    print()
    
    # Display results
    print("=" * 80)
    print("Results Summary")
    print("=" * 80)
    print()
    
    df = engine.get_results_dataframe()
    print(df.to_string(index=False))
    print()
    
    # Display statistics
    stats = engine.get_summary_stats()
    print("=" * 80)
    print("Statistics")
    print("=" * 80)
    print(f"Total Tests: {stats['total_tests']}")
    print(f"Successful: {stats['successful_tests']}")
    print(f"Failed: {stats['failed_tests']}")
    print(f"Average Latency: {stats['avg_latency']:.2f}s")
    print(f"Total Tokens: {stats['total_tokens']}")
    print()
    
    print("Per-Model Statistics:")
    for model_name, model_stats in stats['model_stats'].items():
        print(f"\n  {model_name}:")
        print(f"    Success Rate: {model_stats['success_rate']*100:.1f}%")
        print(f"    Avg Latency: {model_stats['avg_latency']:.2f}s")
        print(f"    Total Tokens: {model_stats['total_tokens']}")
    
    print()
    print("=" * 80)
    print("Sample Detailed Result")
    print("=" * 80)
    
    # Show first result in detail
    if results:
        result = results[0]
        print(f"\nModel: {result.model_name}")
        print(f"Test: {result.test_name}")
        print(f"Prompt: {result.prompt}")
        print(f"\nResponse:\n{result.response}")
        print(f"\nLatency: {result.latency:.2f}s | Tokens: {result.tokens_used}")
    
    print()
    print("=" * 80)
    print("Demo test completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    test_benchmark_engine()
