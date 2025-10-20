"""
Gradio UI for the AI Benchmark application
"""

import gradio as gr
import os
from typing import List, Dict, Any
import json
import pandas as pd

from config import ModelConfig, BenchmarkTest, DEFAULT_TESTS
from benchmark import BenchmarkEngine


class BenchmarkUI:
    """Gradio UI for the benchmark application"""
    
    def __init__(self):
        self.engine = BenchmarkEngine()
        self.custom_tests = []
        self.active_models = []
    
    def add_model(self, name: str, provider: str, model_id: str, enabled: bool, params_json: str) -> str:
        """Add a model to the benchmark"""
        try:
            params = json.loads(params_json) if params_json.strip() else {}
            
            config = ModelConfig(
                name=name,
                provider=provider,
                model_id=model_id,
                enabled=enabled,
                params=params
            )
            
            success = self.engine.add_model(config)
            if success:
                self.active_models.append(name)
                return f"✓ Successfully added model: {name}"
            else:
                return f"✗ Failed to add model: {name}"
        except Exception as e:
            return f"✗ Error adding model: {str(e)}"
    
    def get_model_list(self) -> str:
        """Get list of active models"""
        if not self.active_models:
            return "No models added yet"
        return "\n".join([f"• {model}" for model in self.active_models])
    
    def add_custom_test(self, name: str, description: str, prompt: str, category: str, max_tokens: int) -> str:
        """Add a custom test"""
        try:
            test = BenchmarkTest(
                name=name,
                description=description,
                prompt=prompt,
                category=category,
                max_tokens=max_tokens
            )
            self.custom_tests.append(test)
            return f"✓ Successfully added test: {name}"
        except Exception as e:
            return f"✗ Error adding test: {str(e)}"
    
    def run_benchmark(self, use_default_tests: bool, use_custom_tests: bool, parallel: bool, progress=gr.Progress()) -> tuple:
        """Run the benchmark"""
        if not self.active_models:
            return "Please add at least one model first", None, None
        
        # Collect tests to run
        tests_to_run = []
        if use_default_tests:
            tests_to_run.extend(DEFAULT_TESTS)
        if use_custom_tests and self.custom_tests:
            tests_to_run.extend(self.custom_tests)
        
        if not tests_to_run:
            return "Please select at least one test suite", None, None
        
        progress(0, desc="Starting benchmark...")
        
        # Run benchmark
        results = self.engine.run_benchmark(tests_to_run, parallel=parallel)
        
        progress(0.8, desc="Processing results...")
        
        # Get results
        df = self.engine.get_results_dataframe()
        summary = self.engine.get_summary_stats()
        
        # Format summary text
        summary_text = f"""
## Benchmark Summary

**Total Tests:** {summary['total_tests']}
**Successful:** {summary['successful_tests']}
**Failed:** {summary['failed_tests']}
**Average Latency:** {summary['avg_latency']:.2f}s
**Total Tokens:** {summary.get('total_tokens', 'N/A')}

### Per-Model Statistics:
"""
        for model_name, stats in summary.get('model_stats', {}).items():
            summary_text += f"\n**{model_name}:**\n"
            summary_text += f"  - Success Rate: {stats['success_rate']*100:.1f}%\n"
            summary_text += f"  - Avg Latency: {stats['avg_latency']:.2f}s\n"
            summary_text += f"  - Total Tokens: {stats.get('total_tokens', 'N/A')}\n"
        
        # Create detailed results text
        detailed_results = "## Detailed Results\n\n"
        for result in results:
            detailed_results += f"### {result.model_name} - {result.test_name}\n\n"
            if result.success:
                detailed_results += f"**Prompt:** {result.prompt}\n\n"
                detailed_results += f"**Response:** {result.response}\n\n"
                detailed_results += f"**Latency:** {result.latency:.2f}s | **Tokens:** {result.tokens_used or 'N/A'}\n\n"
            else:
                detailed_results += f"**Error:** {result.error}\n\n"
            detailed_results += "---\n\n"
        
        progress(1.0, desc="Complete!")
        
        return summary_text, df, detailed_results
    
    def clear_all(self) -> str:
        """Clear all models and results"""
        self.engine = BenchmarkEngine()
        self.active_models = []
        self.custom_tests = []
        return "All data cleared"
    
    def create_ui(self) -> gr.Blocks:
        """Create the Gradio UI"""
        
        with gr.Blocks(title="AI Benchmark", theme=gr.themes.Soft()) as app:
            gr.Markdown("# 🤖 AI Benchmark - LLM Model Comparison")
            gr.Markdown("Compare performance across ChatGPT, Gemini, Claude, Grok, and local models (LLaMA, Qwen, Gemma)")
            
            with gr.Tabs():
                # Tab 1: Model Configuration
                with gr.Tab("📋 Configure Models"):
                    gr.Markdown("## Add Models to Benchmark")
                    gr.Markdown("Add API-based models (OpenAI, Anthropic, Google, xAI) or local models using llama.cpp")
                    
                    with gr.Row():
                        with gr.Column(scale=2):
                            model_name = gr.Textbox(label="Model Name", placeholder="e.g., GPT-4")
                            provider = gr.Dropdown(
                                label="Provider",
                                choices=["openai", "anthropic", "google", "xai", "local"],
                                value="openai"
                            )
                            model_id = gr.Textbox(
                                label="Model ID / Path",
                                placeholder="e.g., gpt-4 or /path/to/model.gguf"
                            )
                            enabled = gr.Checkbox(label="Enabled", value=True)
                            params_json = gr.Textbox(
                                label="Parameters (JSON)",
                                placeholder='{"temperature": 0.7}',
                                lines=3
                            )
                            add_model_btn = gr.Button("Add Model", variant="primary")
                        
                        with gr.Column(scale=1):
                            model_status = gr.Textbox(label="Status", interactive=False)
                            active_models_display = gr.Textbox(
                                label="Active Models",
                                interactive=False,
                                lines=10
                            )
                    
                    add_model_btn.click(
                        fn=self.add_model,
                        inputs=[model_name, provider, model_id, enabled, params_json],
                        outputs=[model_status]
                    ).then(
                        fn=self.get_model_list,
                        outputs=[active_models_display]
                    )
                    
                    gr.Markdown("### Quick Setup Examples")
                    with gr.Accordion("Example Configurations", open=False):
                        gr.Markdown("""
**OpenAI (ChatGPT):**
- Model Name: `GPT-3.5`
- Provider: `openai`
- Model ID: `gpt-3.5-turbo`

**Anthropic (Claude):**
- Model Name: `Claude-3-Sonnet`
- Provider: `anthropic`
- Model ID: `claude-3-sonnet-20240229`

**Google (Gemini):**
- Model Name: `Gemini-Pro`
- Provider: `google`
- Model ID: `gemini-pro`

**xAI (Grok):**
- Model Name: `Grok`
- Provider: `xai`
- Model ID: `grok-beta`

**Local Model (LLaMA via llama.cpp):**
- Model Name: `LLaMA-2-7B`
- Provider: `local`
- Model ID: `/path/to/llama-2-7b-chat.Q4_K_M.gguf`
                        """)
                
                # Tab 2: Test Configuration
                with gr.Tab("🧪 Configure Tests"):
                    gr.Markdown("## Default Tests")
                    gr.Markdown("The application includes 5 default tests covering various capabilities:")
                    
                    default_tests_display = gr.Dataframe(
                        value=pd.DataFrame([
                            {"Name": t.name, "Category": t.category, "Description": t.description}
                            for t in DEFAULT_TESTS
                        ]),
                        interactive=False
                    )
                    
                    gr.Markdown("## Add Custom Tests")
                    with gr.Row():
                        with gr.Column():
                            test_name = gr.Textbox(label="Test Name")
                            test_description = gr.Textbox(label="Description")
                            test_prompt = gr.Textbox(label="Prompt", lines=5)
                            test_category = gr.Textbox(label="Category", value="custom")
                            test_max_tokens = gr.Slider(
                                label="Max Tokens",
                                minimum=50,
                                maximum=2000,
                                value=500,
                                step=50
                            )
                            add_test_btn = gr.Button("Add Custom Test", variant="primary")
                            test_status = gr.Textbox(label="Status", interactive=False)
                    
                    add_test_btn.click(
                        fn=self.add_custom_test,
                        inputs=[test_name, test_description, test_prompt, test_category, test_max_tokens],
                        outputs=[test_status]
                    )
                
                # Tab 3: Run Benchmark
                with gr.Tab("▶️ Run Benchmark"):
                    gr.Markdown("## Run Benchmarks")
                    
                    with gr.Row():
                        use_default = gr.Checkbox(label="Use Default Tests", value=True)
                        use_custom = gr.Checkbox(label="Use Custom Tests", value=False)
                        parallel = gr.Checkbox(label="Run in Parallel", value=False)
                    
                    run_btn = gr.Button("🚀 Start Benchmark", variant="primary", size="lg")
                    
                    gr.Markdown("## Results")
                    
                    summary_output = gr.Markdown(label="Summary")
                    results_table = gr.Dataframe(label="Results Table")
                    detailed_output = gr.Markdown(label="Detailed Results")
                    
                    run_btn.click(
                        fn=self.run_benchmark,
                        inputs=[use_default, use_custom, parallel],
                        outputs=[summary_output, results_table, detailed_output]
                    )
                
                # Tab 4: Settings
                with gr.Tab("⚙️ Settings"):
                    gr.Markdown("## Application Settings")
                    gr.Markdown("### Environment Variables")
                    gr.Markdown("""
Set the following environment variables in a `.env` file:

```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
XAI_API_KEY=your_xai_key
```

For local models, download GGUF format models from HuggingFace and specify the path.
                    """)
                    
                    clear_btn = gr.Button("Clear All Data", variant="stop")
                    clear_status = gr.Textbox(label="Status", interactive=False)
                    
                    clear_btn.click(
                        fn=self.clear_all,
                        outputs=[clear_status]
                    ).then(
                        fn=self.get_model_list,
                        outputs=[active_models_display]
                    )
        
        return app


def main():
    """Main entry point"""
    ui = BenchmarkUI()
    app = ui.create_ui()
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
