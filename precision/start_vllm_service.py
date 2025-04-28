"""使用vLLM启动模型API服务并自动测试

支持启动/media/zqj/sda3/deepseek目录下的DeepSeek蒸馏模型服务
并自动执行iquiz评测
"""
import argparse
import subprocess
import time
import requests
from pathlib import Path

MODEL_PATHS = {
    '1.5b': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-1.5B',
    '7b': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-7B',
    '7b-int4': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-7B-GPTQ-Int4',
    '14b': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-14B',
    '14b-int4': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-14B-GPTQ-Int4', 
    '32b': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-32B',
    '32b-int4': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int4',
    '32b-int8': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8',
    '70b': '/media/zqj/sda3/deepseek/DeepSeek-R1-Distill-Llama-70B'
}

def check_service_ready(port: int, timeout: int = 600
):
    """检查服务是否就绪"""
    start_time = time.time()
    url = f"http://127.0.0.1:{port}/v1/models"
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"服务已就绪: {response.json()}")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(5)
        print("等待服务启动...")
    
    print(f"服务启动超时({timeout}秒)")
    return False

def run_eval(model_size: str, port: int):
    """执行评测"""
    cmd = [
        'evalscope', 'eval',
        '--model', f'ds-{model_size}',
        '--api-url',f'http://127.0.0.1:{port}/v1',
        '--api-key', 'EMPTY',
        '--eval-type', 'service',
        '--datasets', 'iquiz'

    ]
    print(f"开始评测模型: {model_size}")
    subprocess.run(cmd)

def start_service(model_size: str, port: int = 8801, gpu_memory_utilization: float = 0.9):
    """启动vLLM API服务并执行评测
    
    Args:
        model_size: 模型大小，如'7b'、'32b-int4'等
        port: 服务端口号，默认8801
        gpu_memory_utilization: GPU内存利用率，默认0.9
    """
    model_path = MODEL_PATHS.get(model_size.lower())
    if not model_path or not Path(model_path).exists():
        raise ValueError(f"模型路径不存在: {model_path}")
    
    max_tp = 3
    for tp in range(2, max_tp + 1):
        # 启动服务
        cmd = [
            'python', '-m', 'vllm.entrypoints.openai.api_server',
            '--model', model_path,
            '--served-model-name', f'ds-{model_size}',
            '--trust-remote-code',
            '--port', str(port),
            '--gpu-memory-utilization', str(gpu_memory_utilization),
            '--max-model-len','8192',
            f'-tp={tp}'
        ]
        
        # GPTQ量化模型需要额外参数
        if 'int' in model_size.lower():
            cmd.extend(['--quantization', 'gptq'])
        
        print(f"\n=== 启动模型服务: {model_size} (tp={tp}) ===")
        print(f"模型路径: {model_path}")
        print(f"访问地址: http://127.0.0.1:{port}/v1")
        
        # 后台启动服务
        process = subprocess.Popen(cmd)
        
        # 等待服务就绪
        if check_service_ready(port):
            # 执行评测
            run_eval(model_size, port)
            # 终止服务
            process.terminate()
            print(f"=== 完成模型 {model_size} 测试 ===")
            return
        
        # 终止服务
        process.terminate()
        print(f"=== tp={tp} 启动失败 ===")
    
    # 所有tp尝试都失败，记录到failed.log
    with open('failed.log', 'a') as f:
        f.write(f"{model_size}\n")
    print(f"=== 模型 {model_size} 所有tp尝试均失败，已记录到failed.log ===")

def main():
    """主函数：自动测试所有模型"""
    models = [
        '14b', '14b-int4',
        '32b', '32b-int4', '32b-int8'
    ]
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8801,
                       help='服务端口号，默认8801')
    parser.add_argument('--gpu-mem', type=float, default=0.9,
                       help='GPU内存利用率，默认0.9')
    
    args = parser.parse_args()
    
    for model in models:
        start_service(model, args.port, args.gpu_mem)

if __name__ == '__main__':
    main()
