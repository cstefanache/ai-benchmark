# Testing Guide

## Quick Test (No API Keys Required)

Run the demo script with mock models to test the benchmark engine:

```bash
python demo.py
```

This will:
- Create mock models that simulate API responses
- Run 3 benchmark tests
- Display results and statistics

## Test with Real Models

### Prerequisites

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up API keys in `.env`:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Test with API Models

1. Edit `example.py` to uncomment the models you want to test
2. Run:
```bash
python example.py
```

### Test with Local Models

1. Download GGUF models from HuggingFace (e.g., TheBloke/Llama-2-7B-Chat-GGUF)
2. Update the path in `example.py`
3. Run:
```bash
python example.py
```

## Run the Gradio UI

```bash
python app.py
```

Then open your browser to `http://localhost:7860`

The UI has 4 tabs:
1. **Configure Models**: Add models to benchmark
2. **Configure Tests**: Use default tests or add custom ones
3. **Run Benchmark**: Execute benchmarks and view results
4. **Settings**: Manage environment and clear data

## Validation Tests

The demo script validates:
- ✅ Core benchmark engine functionality
- ✅ Model adapter interface
- ✅ Test execution and result collection
- ✅ Statistics calculation
- ✅ Result formatting and display

## Expected Output

When running `python demo.py`, you should see:
- Model addition confirmations
- Progress updates during test execution
- Results table with latency and token counts
- Summary statistics per model
- Sample detailed result

All 9 tests (3 models × 3 tests) should complete successfully.
