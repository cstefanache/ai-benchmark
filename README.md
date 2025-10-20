# AI Benchmark - LLM Model Comparison Tool

A comprehensive benchmarking application for comparing multiple Large Language Models (LLMs) including ChatGPT, Gemini, Claude, Grok, and local models (LLaMA, Qwen, Gemma) using llama.cpp.

## Features

- 🤖 **Multiple Model Support**
  - Cloud APIs: OpenAI (ChatGPT), Anthropic (Claude), Google (Gemini), xAI (Grok)
  - Local Models: LLaMA, Qwen, Gemma via llama.cpp
  
- 🧪 **Flexible Benchmark Tests**
  - 5 built-in tests covering coding, creative writing, reasoning, math, and summarization
  - Easy addition of custom tests
  
- 📊 **Comprehensive Results**
  - Latency measurements
  - Token usage tracking
  - Success rate statistics
  - Detailed response comparison
  
- 🎨 **User-Friendly Interface**
  - Built with Gradio
  - Easy model configuration
  - Real-time benchmark execution
  - Export results

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cstefanache/ai-benchmark.git
cd ai-benchmark
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Configuration

### API Keys

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
XAI_API_KEY=your_xai_grok_api_key_here
```

### Local Models

For local models, download GGUF format models from HuggingFace:

1. Visit [HuggingFace](https://huggingface.co/models?library=gguf)
2. Download quantized models (e.g., Q4_K_M variants for good balance of size/quality)
3. Place them in a `models/` directory
4. Reference the path when adding models in the UI

Example models:
- LLaMA 2: `TheBloke/Llama-2-7B-Chat-GGUF`
- Qwen: `Qwen/Qwen-7B-Chat-GGUF`
- Gemma: `google/gemma-7b-it-GGUF`

## Usage

Run the application:

```bash
python app.py
```

Then open your browser to `http://localhost:7860`

### Quick Start Guide

1. **Configure Models** (Tab 1)
   - Add models you want to benchmark
   - For API models, provide the model ID
   - For local models, provide the path to the GGUF file

2. **Configure Tests** (Tab 2)
   - Use default tests or add custom ones
   - Each test has a prompt, category, and token limit

3. **Run Benchmark** (Tab 3)
   - Select which test suites to run
   - Click "Start Benchmark"
   - View results in summary and detailed formats

## Architecture

```
ai-benchmark/
├── app.py           # Main Gradio application
├── benchmark.py     # Benchmark engine
├── models.py        # Model adapters for different providers
├── config.py        # Configuration and data models
├── requirements.txt # Python dependencies
└── .env.example     # Environment variable template
```

## Model Adapters

The application supports the following providers through dedicated adapters:

- **OpenAIAdapter**: ChatGPT models (gpt-3.5-turbo, gpt-4, etc.)
- **AnthropicAdapter**: Claude models (claude-3-opus, claude-3-sonnet, etc.)
- **GoogleAdapter**: Gemini models (gemini-pro, gemini-1.5-pro, etc.)
- **XAIAdapter**: Grok models (grok-beta, etc.)
- **LocalLlamaAdapter**: Local models via llama.cpp (LLaMA, Qwen, Gemma, etc.)

## Benchmark Tests

Default tests include:

1. **Code Generation**: Test coding capabilities
2. **Creative Writing**: Test creative text generation
3. **Logical Reasoning**: Test reasoning abilities
4. **Math Problem**: Test mathematical problem-solving
5. **Summarization**: Test text summarization

You can add custom tests through the UI to test specific capabilities.

## Results

The benchmark provides:

- **Summary Statistics**: Overall success rates, average latency, token usage
- **Per-Model Stats**: Individual model performance metrics
- **Detailed Results**: Full prompts and responses for each test
- **Comparison Table**: Side-by-side comparison of all models

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Gradio](https://gradio.app/)
- Local model support via [llama.cpp](https://github.com/ggerganov/llama.cpp)
- LlamaIndex for advanced LLM capabilities
- API integrations with OpenAI, Anthropic, Google, and xAI