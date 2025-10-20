"""
Simple example script showing how to use the AI Benchmark programmatically
"""

from config import ModelConfig, BenchmarkTest
from benchmark import BenchmarkEngine


def example_with_api_models():
    """Example using API models (requires API keys in .env)"""
    print("Example: Benchmarking with API Models")
    print("=" * 60)
    
    engine = BenchmarkEngine()
    
    # Add models (make sure you have API keys in .env)
    models = [
        ModelConfig(
            name="GPT-3.5",
            provider="openai",
            model_id="gpt-3.5-turbo",
            enabled=True,
            params={"temperature": 0.7}
        ),
        # Uncomment to add more models:
        # ModelConfig(
        #     name="Claude-3",
        #     provider="anthropic",
        #     model_id="claude-3-sonnet-20240229",
        #     enabled=True
        # ),
        # ModelConfig(
        #     name="Gemini-Pro",
        #     provider="google",
        #     model_id="gemini-pro",
        #     enabled=True
        # ),
    ]
    
    for model in models:
        success = engine.add_model(model)
        if success:
            print(f"✓ Added {model.name}")
        else:
            print(f"✗ Failed to add {model.name}")
    
    # Define a simple test
    tests = [
        BenchmarkTest(
            name="Simple Question",
            description="Test basic Q&A",
            prompt="What is the capital of France?",
            category="knowledge",
            max_tokens=50
        )
    ]
    
    print(f"\nRunning {len(tests)} test(s) on {len(engine.models)} model(s)...")
    
    # Run benchmark
    results = engine.run_benchmark(tests, parallel=False)
    
    # Display results
    print("\nResults:")
    print("-" * 60)
    for result in results:
        if result.success:
            print(f"\nModel: {result.model_name}")
            print(f"Response: {result.response}")
            print(f"Latency: {result.latency:.2f}s")
        else:
            print(f"\nModel: {result.model_name}")
            print(f"Error: {result.error}")
    
    print("\n" + "=" * 60)


def example_with_local_model():
    """Example using a local model (requires downloaded GGUF file)"""
    print("Example: Benchmarking with Local Model")
    print("=" * 60)
    
    engine = BenchmarkEngine()
    
    # Add a local model (update path to your model)
    model = ModelConfig(
        name="Local-LLaMA",
        provider="local",
        model_id="/path/to/your/model.gguf",  # Update this path!
        enabled=True,
        params={"n_ctx": 2048, "temperature": 0.7}
    )
    
    success = engine.add_model(model)
    if success:
        print(f"✓ Added {model.name}")
    else:
        print(f"✗ Failed to add {model.name} (check if model file exists)")
        return
    
    # Define a test
    tests = [
        BenchmarkTest(
            name="Code Task",
            description="Simple coding task",
            prompt="Write a Python function that returns the sum of two numbers.",
            category="coding",
            max_tokens=200
        )
    ]
    
    print(f"\nRunning {len(tests)} test(s)...")
    
    # Run benchmark
    results = engine.run_benchmark(tests, parallel=False)
    
    # Display results
    print("\nResults:")
    print("-" * 60)
    for result in results:
        if result.success:
            print(f"\nModel: {result.model_name}")
            print(f"Response: {result.response}")
            print(f"Latency: {result.latency:.2f}s")
        else:
            print(f"\nModel: {result.model_name}")
            print(f"Error: {result.error}")
    
    print("\n" + "=" * 60)


def main():
    print("\n" + "=" * 60)
    print("AI Benchmark - Example Usage")
    print("=" * 60 + "\n")
    
    print("Choose an example:")
    print("1. API Models (requires API keys)")
    print("2. Local Model (requires GGUF file)")
    print("3. Skip examples (run demo.py for mock testing)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        example_with_api_models()
    elif choice == "2":
        example_with_local_model()
    else:
        print("\nTip: Run 'python demo.py' to test with mock models")
        print("Tip: Run 'python app.py' to launch the Gradio UI")


if __name__ == "__main__":
    main()
