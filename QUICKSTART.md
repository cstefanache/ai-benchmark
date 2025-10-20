# Quick Start Guide

Get started with AI Benchmark in 5 minutes!

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/cstefanache/ai-benchmark.git
cd ai-benchmark

# 2. Install dependencies
pip install -r requirements.txt
```

## Try it Now (No API Keys Needed)

Test the application without any API keys:

```bash
python demo.py
```

This runs a demo with mock models to show you how the benchmark works.

## Run with Real Models

### For API Models (OpenAI, Claude, Gemini, Grok)

```bash
# 1. Set up your API keys
cp .env.example .env
# Edit .env and add your API keys

# 2. Start the web interface
python app.py
# or use the startup script
./run.sh          # On Linux/Mac
run.bat           # On Windows

# 3. Open browser
# Go to http://localhost:7860
```

### For Local Models (LLaMA, Qwen, Gemma)

```bash
# 1. Download a GGUF model
# Visit https://huggingface.co/TheBloke
# Download a Q4_K_M model (good balance of size/quality)

# 2. Start the application
python app.py

# 3. In the UI:
# - Provider: local
# - Model ID: /path/to/your/model.gguf
```

## Quick Example (Python Script)

```python
from config import ModelConfig, BenchmarkTest
from benchmark import BenchmarkEngine

# Create engine
engine = BenchmarkEngine()

# Add model (requires OPENAI_API_KEY in .env)
model = ModelConfig(
    name="GPT-3.5",
    provider="openai",
    model_id="gpt-3.5-turbo",
    enabled=True
)
engine.add_model(model)

# Create test
test = BenchmarkTest(
    name="Hello Test",
    description="Simple greeting",
    prompt="Say hello in 3 different languages",
    category="language",
    max_tokens=100
)

# Run and view results
results = engine.run_benchmark([test])
print(results[0].response)
```

## What's Next?

- Read the [User Guide](USER_GUIDE.md) for detailed instructions
- See [Testing Guide](TESTING.md) for testing tips
- Check `example.py` for more code examples
- Explore the default tests in the web UI

## Common Commands

```bash
# Run demo (no API keys needed)
python demo.py

# Run web interface
python app.py

# Run with custom examples
python example.py

# Install dependencies
pip install -r requirements.txt
```

## Getting Help

- Check [USER_GUIDE.md](USER_GUIDE.md) for detailed documentation
- Report issues on GitHub: https://github.com/cstefanache/ai-benchmark/issues

## Features at a Glance

✅ Compare multiple LLMs side-by-side
✅ Support for ChatGPT, Claude, Gemini, Grok
✅ Run local models (LLaMA, Qwen, Gemma)
✅ 5 built-in benchmark tests
✅ Create custom tests
✅ Track latency and token usage
✅ Easy-to-use web interface
✅ Export results

Happy benchmarking! 🚀
