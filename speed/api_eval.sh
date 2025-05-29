#evalscope perf  --parallel 5 --url http://127.0.0.1:8080/v1/completions  --model /media/zqj/sda3/ggml-model-Q4_0.gguf  --log-every-n-query 5  --connect-timeout 6000  --read-timeout 6000  --max-tokens 2048  --min-tokens 2048  --api openai  --dataset speed_benchmark 

CUDA_VISIBLE_DEVICES=0,1 evalscope perf \
 --parallel 32 \
 --model Qwen/Qwen2.5-0.5B-Instruct \
 --log-every-n-query 5 \
 --connect-timeout 6000 \
 --read-timeout 6000 \
 --max-tokens 4096 \
 --min-tokens 512 \
 --api local_vllm \
 --dataset speed_benchmark 
