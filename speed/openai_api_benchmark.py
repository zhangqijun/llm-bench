"""Benchmark OpenAI compatible API performance."""
import argparse
import asyncio
import json
import time
from typing import List, Dict, Tuple
import aiohttp
import numpy as np

class BenchmarkStats:
    def __init__(self):
        self.request_times = []
        self.ttft_times = []
        self.completion_times = []
        self.success_count = 0
        self.failure_count = 0
    
    def add_result(self, success: bool, ttft: float, completion_time: float):
        if success:
            self.success_count += 1
            self.ttft_times.append(ttft)
            self.completion_times.append(completion_time)
            self.request_times.append(completion_time)
        else:
            self.failure_count += 1
    
    def calculate_stats(self) -> Dict[str, float]:
        if not self.success_count:
            return {
                "success_rate": 0.0,
                "avg_ttft": 0.0,
                "avg_completion_time": 0.0,
                "tps": 0.0,
                "p50_ttft": 0.0,
                "p90_ttft": 0.0,
                "p95_ttft": 0.0,
                "p50_completion": 0.0,
                "p90_completion": 0.0,
                "p95_completion": 0.0
            }
        
        return {
            "success_rate": self.success_count / (self.success_count + self.failure_count),
            "avg_ttft": np.mean(self.ttft_times),
            "avg_completion_time": np.mean(self.completion_times),
            "tps": self.success_count / np.sum(self.request_times),
            "p50_ttft": np.percentile(self.ttft_times, 50),
            "p90_ttft": np.percentile(self.ttft_times, 90),
            "p95_ttft": np.percentile(self.ttft_times, 95),
            "p50_completion": np.percentile(self.completion_times, 50),
            "p90_completion": np.percentile(self.completion_times, 90),
            "p95_completion": np.percentile(self.completion_times, 95)
        }

async def make_request(
    session: aiohttp.ClientSession,
    api_url: str,
    api_key: str,
    prompt: str,
    max_tokens: int,
    stream: bool,
    args: argparse.Namespace
) -> Tuple[bool, float, float]:
    headers = {
        "Content-Type": "application/json"
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if args.ollama:
        payload = {
            "model": args.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "stream": stream,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
    elif args.vllm:
        payload = {
            "model": args.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "stream": stream,
            "temperature": 0.7  # vLLM常用默认参数
        }
    else:
        payload = {
            "model": args.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "stream": stream
        }
    
    start_time = time.time()
    ttft = 0.0
    success = False
    
    try:
        timeout = aiohttp.ClientTimeout(total=120)  # 增加超时到120秒
        if stream:
            async with session.post(api_url, json=payload, headers=headers, timeout=timeout) as response:
                print(f"Request started to {api_url}")  # 调试信息
                if response.status != 200:
                    error_content = await response.text()
                    print(f"Request failed with status {response.status}: {error_content}")
                    return (False, 0.0, 0.0)
                
                # Measure time to first token
                first_chunk = True
                first_token_time = None
                async for chunk in response.content:
                    if first_chunk:
                        first_token_time = time.time()
                        ttft = first_token_time - start_time
                        print(f"First token received in {ttft:.2f}s")  # 调试信息
                        first_chunk = False
                    
                    try:
                        # 直接处理chunk内容，不再await
                        chunk_str = chunk.decode('utf-8')
                        # 解析streaming响应中的JSON数据
                        for line in chunk_str.split('\n'):
                            if line.startswith('data:'):
                                try:
                                    data = json.loads(line[5:])
                                    if 'response' in data:
                                        print(f"Stream response: {data['response']}", end='')
                                except json.JSONDecodeError:
                                    pass
                    except Exception as e:
                        print(f"Error processing chunk: {str(e)}")
                        return (False, ttft, time.time() - start_time)
                
                completion_time = time.time() - start_time
                print(f"\nRequest completed in {completion_time:.2f}s")  # 调试信息
                success = True
        else:
            async with session.post(api_url, json=payload, headers=headers, timeout=timeout) as response:
                print(f"Request started to {api_url}")  # 调试信息
                if response.status != 200:
                    print(f"Request failed with status {response.status}")
                    return (False, 0.0, 0.0)
                
                ttft = time.time() - start_time
                print(f"First token received in {ttft:.2f}s")  # 调试信息
                await response.json()
                completion_time = time.time() - start_time
                print(f"Request completed in {completion_time:.2f}s")  # 调试信息
                success = True
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return (False, 0.0, 0.0)
    
    return (success, ttft, completion_time)

async def worker(
    session: aiohttp.ClientSession,
    api_url: str,
    api_key: str,
    prompts: List[str],
    max_tokens: int,
    stream: bool,
    stats: BenchmarkStats,
    args: argparse.Namespace
):
    for prompt in prompts:
        success, ttft, completion_time = await make_request(
            session, api_url, api_key, prompt, max_tokens, stream, args
        )
        stats.add_result(success, ttft, completion_time)

async def run_benchmark(
    api_url: str,
    api_key: str,
    prompts: List[str],
    max_tokens: int,
    concurrency: int,
    stream: bool,
    args: argparse.Namespace
) -> BenchmarkStats:
    stats = BenchmarkStats()
    connector = aiohttp.TCPConnector(limit=concurrency)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        prompts_per_worker = len(prompts) // concurrency
        
        for i in range(concurrency):
            start = i * prompts_per_worker
            end = (i + 1) * prompts_per_worker if i < concurrency - 1 else len(prompts)
            worker_prompts = prompts[start:end]
            
            task = asyncio.create_task(
                worker(session, api_url, api_key, worker_prompts, max_tokens, stream, stats, args)
            )
            tasks.append(task)
        
        await asyncio.gather(*tasks)
    
    return stats

def generate_prompts(num_prompts: int, prompt_length: int) -> List[str]:
    return [
        ("Tell me a story about AI." * (prompt_length // 20 + 1))[:prompt_length]
        for _ in range(num_prompts)
    ]

async def validate_connection(api_url: str, api_key: str, args: argparse.Namespace) -> bool:
    """Validate API connection with a single test request."""
    connector = aiohttp.TCPConnector()
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            test_prompt = "Test connection"
            success, _, _ = await make_request(
                session, api_url, api_key, test_prompt, 10, False, args
            )
            if not success:
                print("❌ Connection test failed")
                return False
            print("✅ Connection test passed")
            return True
    except Exception as e:
        print(f"❌ Connection test error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Benchmark OpenAI compatible API performance.")
    parser.add_argument("--api-url", type=str, required=True, help="API endpoint URL (e.g. http://localhost:11434 for Ollama)")
    parser.add_argument("--api-key", type=str, default="", help="API key for authentication (not required for Ollama)")
    parser.add_argument("--ollama", action="store_true", help="Use Ollama API format")
    parser.add_argument("--vllm", action="store_true", help="Use vLLM API format")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model name to use")
    parser.add_argument("--num-prompts", type=int, default=100, help="Total number of prompts to send")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent requests")
    parser.add_argument("--prompt-length", type=int, default=100, help="Approximate length of each prompt in characters")
    parser.add_argument("--max-tokens", type=int, default=100, help="Maximum number of tokens to generate per request")
    parser.add_argument("--stream", action="store_true", help="Use streaming API")
    parser.add_argument("--output", type=str, help="Path to save benchmark results in JSON format")
    
    args = parser.parse_args()
    
    # 先执行连接测试
    print("Running connection test...")
    if not asyncio.run(validate_connection(args.api_url, args.api_key, args)):
        print("Aborting benchmark due to connection failure")
        return
    
    print("Generating test prompts...")
    prompts = generate_prompts(args.num_prompts, args.prompt_length)
    
    print(f"Starting benchmark with {args.concurrency} concurrent workers...")
    start_time = time.time()
    stats = asyncio.run(run_benchmark(
        args.api_url, args.api_key, prompts, args.max_tokens, args.concurrency, args.stream, args
    ))
    total_time = time.time() - start_time
    
    results = stats.calculate_stats()
    results["total_time"] = total_time
    results["total_requests"] = args.num_prompts
    results["concurrency"] = args.concurrency
    
    print("\nBenchmark Results:")
    print(f"  Success rate: {results['success_rate']:.2%}")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Requests per second (TPS): {results['tps']:.2f}")
    print(f"  Average TTFT: {results['avg_ttft'] * 1000:.2f}ms")
    print(f"  Average completion time: {results['avg_completion_time'] * 1000:.2f}ms")
    print("\nPercentiles (TTFT):")
    print(f"  p50: {results['p50_ttft'] * 1000:.2f}ms")
    print(f"  p90: {results['p90_ttft'] * 1000:.2f}ms")
    print(f"  p95: {results['p95_ttft'] * 1000:.2f}ms")
    print("\nPercentiles (Completion Time):")
    print(f"  p50: {results['p50_completion'] * 1000:.2f}ms")
    print(f"  p90: {results['p90_completion'] * 1000:.2f}ms")
    print(f"  p95: {results['p95_completion'] * 1000:.2f}ms")
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    import sys
    
    # 检查是否传入了--ollama和--model参数
    if "--ollama" in sys.argv and "--model" in sys.argv:
        # 设置默认Ollama参数
        if "--api-url" not in sys.argv:
            sys.argv.append("--api-url=http://localhost:11434/api/generate")
        if "--api-key" not in sys.argv:
            sys.argv.append("--api-key=")
    
    main()
