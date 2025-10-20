# User Guide - AI Benchmark

## Overview

The AI Benchmark application allows you to compare the performance of multiple Large Language Models (LLMs) across various tasks. It supports both cloud-based APIs and local models.

## Supported Models

### Cloud APIs
- **OpenAI**: GPT-3.5, GPT-4, and other ChatGPT models
- **Anthropic**: Claude 3 (Opus, Sonnet, Haiku)
- **Google**: Gemini Pro, Gemini 1.5 Pro
- **xAI**: Grok models

### Local Models (via llama.cpp)
- **LLaMA**: LLaMA 2, LLaMA 3, Code LLaMA
- **Qwen**: Qwen 1.5, Qwen 2
- **Gemma**: Gemma 2B, Gemma 7B
- Any other GGUF format model

## Getting Started

### 1. Installation

```bash
git clone https://github.com/cstefanache/ai-benchmark.git
cd ai-benchmark
pip install -r requirements.txt
```

### 2. Configuration

#### For API Models

Create a `.env` file with your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AI...
XAI_API_KEY=xai-...
```

#### For Local Models

1. Download GGUF models from HuggingFace:
   - Visit https://huggingface.co/models?library=gguf
   - Search for quantized models (look for Q4_K_M for good balance)
   - Download to a `models/` directory

2. Recommended models:
   - [TheBloke/Llama-2-7B-Chat-GGUF](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)
   - [Qwen/Qwen1.5-7B-Chat-GGUF](https://huggingface.co/Qwen/Qwen1.5-7B-Chat-GGUF)
   - [google/gemma-7b-it-GGUF](https://huggingface.co/google/gemma-7b-it-GGUF)

### 3. Running the Application

#### Option A: Gradio Web UI (Recommended)

```bash
python app.py
```

Open your browser to `http://localhost:7860`

#### Option B: Python Script

```python
from config import ModelConfig, BenchmarkTest
from benchmark import BenchmarkEngine

# Create engine
engine = BenchmarkEngine()

# Add a model
model = ModelConfig(
    name="GPT-3.5",
    provider="openai",
    model_id="gpt-3.5-turbo",
    enabled=True,
    params={"temperature": 0.7}
)
engine.add_model(model)

# Define a test
test = BenchmarkTest(
    name="Simple Test",
    description="Basic question",
    prompt="What is 2+2?",
    category="math",
    max_tokens=50
)

# Run benchmark
results = engine.run_benchmark([test])

# View results
for result in results:
    print(f"{result.model_name}: {result.response}")
    print(f"Latency: {result.latency:.2f}s")
```

#### Option C: Demo (No API Keys)

Test the framework without API keys:

```bash
python demo.py
```

## Using the Gradio UI

### Tab 1: Configure Models

1. Enter a descriptive name for the model
2. Select the provider (openai, anthropic, google, xai, or local)
3. Enter the model ID:
   - For APIs: `gpt-3.5-turbo`, `claude-3-sonnet-20240229`, `gemini-pro`, `grok-beta`
   - For local: Full path to GGUF file (e.g., `/home/user/models/llama-2-7b.gguf`)
4. (Optional) Add parameters as JSON: `{"temperature": 0.7, "top_p": 0.9}`
5. Click "Add Model"

**Tips:**
- Add multiple models to compare them side-by-side
- Local models may take longer to load the first time
- You can disable/enable models by toggling the checkbox

### Tab 2: Configure Tests

The app includes 5 default tests:
- **Code Generation**: Tests programming ability
- **Creative Writing**: Tests creativity
- **Logical Reasoning**: Tests reasoning skills
- **Math Problem**: Tests mathematical abilities
- **Summarization**: Tests text summarization

**Adding Custom Tests:**
1. Enter a test name
2. Write a description
3. Write the prompt
4. Set a category (for organization)
5. Adjust max tokens (controls response length)
6. Click "Add Custom Test"

### Tab 3: Run Benchmark

1. Select which test suites to run:
   - ☑️ Use Default Tests (recommended)
   - ☐ Use Custom Tests (if you added any)

2. Choose execution mode:
   - ☐ Run in Parallel: Faster but uses more resources
   - ☑️ Run Sequentially: Safer for rate limits

3. Click "🚀 Start Benchmark"

**Results Display:**
- **Summary**: High-level statistics (success rate, average latency, tokens)
- **Results Table**: Tabular view of all test runs
- **Detailed Results**: Full prompts and responses

### Tab 4: Settings

- View environment configuration help
- Clear all data to start fresh

## Understanding Results

### Metrics

- **Latency**: Time taken to generate response (in seconds)
- **Tokens**: Number of tokens used (if available)
- **Success Rate**: Percentage of successful completions
- **Response Length**: Number of characters in response

### Interpreting Results

**Latency Comparison:**
- Lower is better for user experience
- Cloud APIs are typically faster for short responses
- Local models may be faster for longer generation

**Quality Assessment:**
- Read the actual responses
- Check if responses address the prompt correctly
- Look for hallucinations or errors
- Consider token efficiency (shorter is often better)

**Cost Considerations:**
- API models charge per token
- Local models have upfront hardware/download costs but no per-use fees
- Check the "Total Tokens" in results to estimate API costs

## Advanced Usage

### Custom Model Parameters

You can customize model behavior using the Parameters JSON field:

```json
{
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 500,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0
}
```

**Common Parameters:**
- `temperature`: Controls randomness (0.0-1.0, lower = more focused)
- `top_p`: Nucleus sampling (0.0-1.0)
- `max_tokens`: Maximum response length

### Local Model Parameters

For local models (via llama.cpp), you can also configure:

```json
{
  "n_ctx": 2048,
  "n_threads": 4,
  "n_gpu_layers": 35,
  "temperature": 0.7
}
```

**Local Model Parameters:**
- `n_ctx`: Context window size (tokens)
- `n_threads`: Number of CPU threads to use
- `n_gpu_layers`: Layers to offload to GPU (requires GPU build)

### Creating Test Suites

For thorough evaluation, create tests across categories:

1. **Technical Skills**
   - Code generation
   - Code debugging
   - Algorithm design

2. **Language Understanding**
   - Reading comprehension
   - Summarization
   - Translation

3. **Reasoning**
   - Logical reasoning
   - Math problems
   - Common sense reasoning

4. **Creative Tasks**
   - Story writing
   - Poetry generation
   - Creative problem-solving

## Troubleshooting

### API Errors

**"API key not found"**
- Check that `.env` file exists and contains your key
- Verify the key name matches (e.g., `OPENAI_API_KEY`)

**"Rate limit exceeded"**
- Reduce the number of concurrent tests
- Disable parallel execution
- Wait and retry

**"Model not found"**
- Verify the model ID is correct
- Check if you have access to the model (e.g., GPT-4 requires special access)

### Local Model Errors

**"Model file not found"**
- Check the file path is absolute and correct
- Verify the file is in GGUF format (not safetensors or other formats)

**"Out of memory"**
- Reduce `n_ctx` parameter
- Use a smaller model (e.g., 7B instead of 13B)
- Use more quantized model (e.g., Q4_K_M instead of Q8_0)

**"Very slow generation"**
- Increase `n_threads` to use more CPU cores
- Build llama-cpp-python with GPU support
- Set `n_gpu_layers` to offload to GPU

### Gradio UI Issues

**"Unable to connect"**
- Check if port 7860 is available
- Try running with `app.launch(server_port=7861)`

## Best Practices

1. **Start Small**: Test with one model and one test first
2. **Use Default Tests**: They cover common use cases
3. **Compare Similar Models**: GPT-3.5 vs Gemini Pro, not GPT-4 vs local 7B model
4. **Consider Context**: Different models excel at different tasks
5. **Monitor Costs**: API calls cost money - be aware of token usage
6. **Save Results**: Copy important benchmark results for later reference

## Example Workflows

### Workflow 1: Find the Best Free Model

1. Add models: Claude Sonnet, Gemini Pro, Grok
2. Run all default tests
3. Compare response quality and latency
4. Choose based on your priorities (speed vs quality)

### Workflow 2: API vs Local Comparison

1. Add API model (e.g., GPT-3.5)
2. Add local model (e.g., LLaMA-2-7B)
3. Run coding and reasoning tests
4. Compare quality, speed, and cost implications

### Workflow 3: Model Selection for Specific Task

1. Create custom tests for your specific use case
2. Add candidate models
3. Run benchmark
4. Analyze which model performs best for your needs

## Support and Resources

- GitHub: https://github.com/cstefanache/ai-benchmark
- Report issues: https://github.com/cstefanache/ai-benchmark/issues
- HuggingFace models: https://huggingface.co/models
- llama.cpp: https://github.com/ggerganov/llama.cpp

## License

MIT License - See LICENSE file for details
