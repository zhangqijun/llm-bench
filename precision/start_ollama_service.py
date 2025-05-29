"""使用Ollama启动模型API服务并自动测试

支持启动Ollama管理的模型服务
并自动执行iquiz评测
"""
import argparse
import subprocess
import time
import requests
from pathlib import Path

MODEL_NAMES = {
    '7b': 'deepseek-r1:7b',
    '14b': 'deepseek-r1:14b', 
    '32b': 'deepseek-r1:32b',
    '70b': 'deepseek-r1:70b',
    'qwq': 'qwq:latest',
    '1.5b-int8': 'deepseek-r1:1.5b-qwen-distill-q8_0',
    '1.5b-fp16': 'deepseek-r1:1.5b-qwen-distill-fp16',
    '1.5b-q4': 'deepseek-r1:1.5b-qwen-distill-q4_K_M',
    '7b-int8': 'deepseek-r1:7b-qwen-distill-q8_0',
    '7b-fp16': 'deepseek-r1:7b-qwen-distill-fp16',
    '7b-q4': 'deepseek-r1:7b-qwen-distill-q4_K_M',
    '8b-int8': 'deepseek-r1:8b-llama-distill-q8_0',
    '8b-fp16': 'deepseek-r1:8b-llama-distill-fp16',
    '8b-q4': 'deepseek-r1:8b-llama-distill-q4_K_M',
    '14b-int8': 'deepseek-r1:14b-qwen-distill-q8_0',
    '14b-fp16': 'deepseek-r1:14b-qwen-distill-fp16',
    '14b-q4': 'deepseek-r1:14b-qwen-distill-q4_K_M',
    '32b-int8': 'deepseek-r1:32b-qwen-distill-q8_0',
    '32b-fp16': 'deepseek-r1:32b-qwen-distill-fp16',
    '32b-q4': 'deepseek-r1:32b-qwen-distill-q4_K_M',
    '70b-int8': 'deepseek-r1:70b-llama-distill-q8_0',
    '70b-fp16': 'deepseek-r1:70b-llama-distill-fp16',
    '70b-q4': 'deepseek-r1:70b-llama-distill-q4_K_M',
    'qwen3_0.6b': 'qwen3:0.6b',
    'qwen3_1.7b': 'qwen3:1.7b',
    'qwen3_4b': 'qwen3:4b',
    'qwen3_8b': 'qwen3:8b',
    'qwen3_14b': 'qwen3:14b',
    'qwen3_30b': 'qwen3:30b',
    'qwen3_32b': 'qwen3:32b',
    'qwen3_0.6b-fp16': 'qwen3:0.6b-fp16',
    'qwen3_0.6b-q8_0': 'qwen3:0.6b-q8_0',
    'qwen3_1.7b-fp16': 'qwen3:1.7b-fp16',
    'qwen3_1.7b-q8_0': 'qwen3:1.7b-q8_0',
    'qwen3_4b-fp16': 'qwen3:4b-fp16',
    'qwen3_4b-q8_0': 'qwen3:4b-q8_0',
    'qwen3_8b-fp16': 'qwen3:8b-fp16',
    'qwen3_8b-q8_0': 'qwen3:8b-q8_0',
    'qwen3_14b-fp16': 'qwen3:14b-fp16',
    'qwen3_14b-q8_0': 'qwen3:14b-q8_0',
    'qwen3_30b-a3b': 'qwen3:30b-a3b',
    'qwen3_30b-a3b-fp16': 'qwen3:30b-a3b-fp16',
    'qwen3_30b-a3b-q8_0': 'qwen3:30b-a3b-q8_0',
    'qwen3_32b-fp16': 'qwen3:32b-fp16',
    'qwen3_32b-q8_0': 'qwen3:32b-q8_0'
}

def check_service_ready(port: int, timeout: int = 3600):
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
    model_name = MODEL_NAMES.get(model_size.lower())
    cmd = [
        'evalscope', 'eval',
        '--model', model_name,
        '--api-url', f'http://127.0.0.1:{port}/v1',
        '--api-key', 'EMPTY',
        '--eval-type', 'service',
        '--datasets', 'iquiz'
    ]
    print(f"开始评测模型: {model_size}")
    subprocess.run(cmd)

def start_service(model_size: str, port: int = 11434):
    """启动Ollama API服务并执行评测
    
    Args:
        model_size: 模型大小，如'7b'、'32b'等
        port: 服务端口号，默认11434
    """
    model_name = MODEL_NAMES.get(model_size.lower())
    if not model_name:
        raise ValueError(f"不支持的模型大小: {model_size}")
    
    # 检查ollama服务是否已运行
    try:
        subprocess.run(['ollama', 'list'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("Ollama服务未运行，请先执行'ollama serve'启动服务")
    
    # 拉取模型(如果不存在)
    subprocess.run(['ollama', 'pull', model_name])
    
    print(f"\n=== 测试模型服务: {model_size} ===")
    print(f"模型名称: {model_name}")
    print(f"访问地址: http://127.0.0.1:{port}/v1")
    
    # 检查服务是否就绪
    if check_service_ready(port):
        # 执行评测
        run_eval(model_size, port)
        print(f"=== 完成模型 {model_size} 测试 ===")
    else:
        print(f"=== 模型 {model_size} 启动失败 ===")
        with open('failed.log', 'a') as f:
            f.write(f"{model_size}\n")

def main():
    """主函数：自动测试所有模型"""
    models = [
        # 'qwen3_30b-a3b-fp16', 'qwen3_4b',
        # 'qwen3_8b', 'qwen3_14b', 'qwen3_30b',
        # 'qwen3_32b', 'qwen3_0.6b-fp16',
        # 'qwen3_0.6b-q8_0', 'qwen3_1.7b-fp16',
        # 'qwen3_1.7b-q8_0', 'qwen3_4b-fp16',
        # 'qwen3_4b-q8_0', 'qwen3_8b-fp16',
        # 'qwen3_8b-q8_0', 'qwen3_14b-fp16',
        # 'qwen3_14b-q8_0', 'qwen3_30b-a3b',
        # 'qwen3_30b-a3b-q8_0',
        'qwen3_32b-fp16', 'qwen3_32b-q8_0'
    ]
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=11434,
                       help='服务端口号，默认11434')
    
    args = parser.parse_args()
    
    for model in models:
        start_service(model, args.port)

if __name__ == '__main__':
    main()
