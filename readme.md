# LLM Bench

A benchmarking tool for evaluating LLM (Large Language Model) performance.

## Features
- Precision testing (located in /precision directory)
- Speed testing (located in /speed directory)

## Latest Benchmark Results (Sorted by IQ+EQ Score)

| Model Name | Date | IQ Score | EQ Score | Parameters | Quantization | Architecture |
|------------|------|---------|---------|------------|-------------|-------------|
| claude-3.7-sonnet | 2025-04-24 15:06:49 | 0.825 | 0.95 | 8.0B | Q4_K_M | claude |
| deepseek-chat | 2025-04-24 14:23:40 | 0.85 | 0.8875 | 70.6B | Q4_K_M | deepseek |
| deepseek-r1-32b-qwen-distill-fp16 | 2025-04-27 21:49:41 | 0.85 | 0.8 | 32.8B | F16 | qwen2 |
| deepseek-r1-32b-qwen-distill-q8_0 | 2025-04-27 21:01:28 | 0.825 | 0.7375 | 32.8B | Q8_0 | qwen2 |
| qwq-latest | 2025-04-25 16:47:10 | 0.8 | 0.7375 | 32.8B | Q4_K_M | qwen2 |
| deepseek-r1-32b-qwen-distill-q4_K_M | 2025-04-27 23:07:59 | 0.75 | 0.725 | 32.8B | Q4_K_M | qwen2 |
| deepseek-r1-32b | 2025-04-25 09:53:02 | 0.75 | 0.725 | 32.8B | Q4_K_M | qwen2 |
| deepseek-r1-70b-llama-distill-q4_K_M | 2025-04-28 06:04:27 | 0.675 | 0.775 | 70.6B | Q4_K_M | llama |
| deepseek-r1-14b-qwen-distill-fp16 | 2025-04-27 19:57:39 | 0.7 | 0.6375 | 14.8B | F16 | qwen2 |
| deepseek-r1-14b-qwen-distill-q8_0 | 2025-04-27 19:30:21 | 0.7 | 0.6375 | 14.8B | Q8_0 | qwen2 |

(Showing top 10 results sorted by IQ+EQ score, full results available in precision/model_scores.csv)

## Directory Structure
- /precision: Contains scripts for model evaluation and scoring
- /speed: Performance benchmarking tools

## Getting Started
1. Clone the repository
2. Run the desired evaluation scripts from the precision or speed directories
