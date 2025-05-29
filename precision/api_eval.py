import subprocess
import time
import requests
import os
import glob
import json
import random

def get_available_models(api_url: str, api_key: str, service: str):
    """获取API可用的模型列表"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 不同服务的模型端点可能不同，这里做一个简单的适配
    models_endpoint = f"{api_url}/models"
    
    try:
        print(f"正在获取 {service} 的可用模型列表...")
        response = requests.get(models_endpoint, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出异常
        
        models_data = response.json()
        
        # 创建data文件夹（如果不存在）
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"创建目录: {data_dir}")
        
        # 保存模型列表到JSON文件
        models_file = os.path.join(data_dir, f"{service}_models.json")
        print(f"获取模型列表失败: {e}")
        return None
    except:pass

def batch_eval(api_key: str, api_url: str):
    """批量评测模型"""
    models = ["gemini-2.5-pro-preview-05-06"]
    """批量评测模型"""
    for model in models:
           
        cmd = [
            'evalscope', 'eval',
            '--model', model,
            '--api-url', api_url,
            '--eval-type', 'service',
            '--datasets', 'iquiz',
            '--api-key', api_key,
            '--stream'
        ]
        print(f"\n开始评测模型: {model}")
        subprocess.run(cmd)
        time.sleep(5)  # 避免请求过于频繁

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', type=str, required=False, default='openrouter',
                       choices=['openrouter', 'modelscope', 'siliconflow','openai','google'],
                       help='指定使用的服务（默认: openrouter）')
    parser.add_argument('--get-models', action='store_true',
                       help='获取并保存可用模型列表')
    parser.add_argument('--eval', action='store_true', help='执行模型评测')
    
    args = parser.parse_args()
    
    # 如果没有指定任何操作，默认执行评测
    if not args.get_models and not args.eval:
        args.eval = True
    
    # 从api_keys.json读取配置
    try:
        with open('../api_keys.json') as f:
            keys = json.load(f)
            service = args.service
            api_key = keys[service]['api_key']
            api_url = keys[service]['api_url']
            print(f"使用服务: {service}")
            print(f"API URL: {api_url}")
            print(f"API密钥: {api_key[:4]}...{api_key[-4:]}")
    except Exception as e:
        print(f"无法从api_keys.json读取配置: {e}")
        exit(1)
    
    # 获取模型列表
    if args.get_models:
        get_available_models(api_url, api_key, service)
    
    # 执行模型评测
    if args.eval:
        batch_eval(api_key, api_url)
