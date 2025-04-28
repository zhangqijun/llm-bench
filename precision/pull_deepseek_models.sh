#!/bin/bash

# Pull all DeepSeek R1 distill models using ollama
ollama pull deepseek-r1:1.5b-qwen-distill-fp16
ollama pull deepseek-r1:1.5b-qwen-distill-q4_K_M
ollama pull deepseek-r1:1.5b-qwen-distill-q8_0
ollama pull deepseek-r1:7b-qwen-distill-fp16
ollama pull deepseek-r1:7b-qwen-distill-q4_K_M
ollama pull deepseek-r1:7b-qwen-distill-q8_0
ollama pull deepseek-r1:8b-llama-distill-fp16
ollama pull deepseek-r1:8b-llama-distill-q4_K_M
ollama pull deepseek-r1:8b-llama-distill-q8_0
ollama pull deepseek-r1:14b-qwen-distill-fp16
ollama pull deepseek-r1:14b-qwen-distill-q4_K_M
ollama pull deepseek-r1:14b-qwen-distill-q8_0
ollama pull deepseek-r1:32b-qwen-distill-fp16
ollama pull deepseek-r1:32b-qwen-distill-q4_K_M
ollama pull deepseek-r1:32b-qwen-distill-q8_0
ollama pull deepseek-r1:70b-llama-distill-q4_K_M
ollama pull deepseek-r1:70b-llama-distill-fp16
ollama pull deepseek-r1:70b-llama-distill-q8_0

echo "所有DeepSeek模型pull命令已生成，请执行此脚本"
