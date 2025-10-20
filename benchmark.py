"""
Benchmark engine for running tests on multiple models
"""

from typing import List, Dict, Optional
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

from config import ModelConfig, BenchmarkTest, BenchmarkResult
from models import (
    ModelAdapter, OpenAIAdapter, AnthropicAdapter, 
    GoogleAdapter, XAIAdapter, LocalLlamaAdapter
)


class BenchmarkEngine:
    """Engine for running benchmarks on multiple models"""
    
    def __init__(self):
        self.models: Dict[str, ModelAdapter] = {}
        self.results: List[BenchmarkResult] = []
    
    def add_model(self, config: ModelConfig) -> bool:
        """Add a model to the benchmark"""
        if not config.enabled:
            return False
        
        try:
            if config.provider == "openai":
                adapter = OpenAIAdapter(config.model_id, config.params)
            elif config.provider == "anthropic":
                adapter = AnthropicAdapter(config.model_id, config.params)
            elif config.provider == "google":
                adapter = GoogleAdapter(config.model_id, config.params)
            elif config.provider == "xai":
                adapter = XAIAdapter(config.model_id, config.params)
            elif config.provider == "local":
                # For local models, model_id is the path
                adapter = LocalLlamaAdapter(config.model_id, config.params)
            else:
                raise ValueError(f"Unknown provider: {config.provider}")
            
            self.models[config.name] = adapter
            return True
        except Exception as e:
            print(f"Error adding model {config.name}: {str(e)}")
            return False
    
    def run_test(self, model_name: str, test: BenchmarkTest) -> BenchmarkResult:
        """Run a single test on a single model"""
        adapter = self.models.get(model_name)
        if not adapter:
            return BenchmarkResult(
                model_name=model_name,
                test_name=test.name,
                prompt=test.prompt,
                response="",
                latency=0,
                success=False,
                error="Model not found"
            )
        
        try:
            response, latency, tokens = adapter.generate(test.prompt, test.max_tokens)
            
            result = BenchmarkResult(
                model_name=model_name,
                test_name=test.name,
                prompt=test.prompt,
                response=response,
                latency=latency,
                tokens_used=tokens,
                success=True
            )
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = BenchmarkResult(
                model_name=model_name,
                test_name=test.name,
                prompt=test.prompt,
                response="",
                latency=0,
                success=False,
                error=str(e)
            )
            self.results.append(result)
            return result
    
    def run_benchmark(self, tests: List[BenchmarkTest], parallel: bool = False) -> List[BenchmarkResult]:
        """Run all tests on all models"""
        results = []
        
        if parallel:
            # Run tests in parallel
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for model_name in self.models.keys():
                    for test in tests:
                        future = executor.submit(self.run_test, model_name, test)
                        futures.append(future)
                
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        print(f"Error in parallel execution: {str(e)}")
        else:
            # Run tests sequentially
            for model_name in self.models.keys():
                for test in tests:
                    result = self.run_test(model_name, test)
                    results.append(result)
        
        return results
    
    def get_results_dataframe(self) -> pd.DataFrame:
        """Convert results to a pandas DataFrame"""
        if not self.results:
            return pd.DataFrame()
        
        data = []
        for result in self.results:
            data.append({
                "Model": result.model_name,
                "Test": result.test_name,
                "Success": result.success,
                "Latency (s)": round(result.latency, 2) if result.success else None,
                "Tokens": result.tokens_used,
                "Response Length": len(result.response) if result.success else 0,
                "Error": result.error if not result.success else None
            })
        
        return pd.DataFrame(data)
    
    def get_summary_stats(self) -> Dict[str, any]:
        """Get summary statistics for the benchmark"""
        if not self.results:
            return {}
        
        df = self.get_results_dataframe()
        
        summary = {
            "total_tests": len(self.results),
            "successful_tests": df["Success"].sum(),
            "failed_tests": (~df["Success"]).sum(),
            "avg_latency": df[df["Success"]]["Latency (s)"].mean() if df["Success"].any() else 0,
            "total_tokens": df["Tokens"].sum() if "Tokens" in df and not df["Tokens"].isna().all() else 0,
        }
        
        # Per-model statistics
        model_stats = {}
        for model_name in df["Model"].unique():
            model_df = df[df["Model"] == model_name]
            model_stats[model_name] = {
                "success_rate": model_df["Success"].mean(),
                "avg_latency": model_df[model_df["Success"]]["Latency (s)"].mean() if model_df["Success"].any() else 0,
                "total_tokens": model_df["Tokens"].sum() if not model_df["Tokens"].isna().all() else 0,
            }
        
        summary["model_stats"] = model_stats
        
        return summary
    
    def clear_results(self):
        """Clear all results"""
        self.results = []
