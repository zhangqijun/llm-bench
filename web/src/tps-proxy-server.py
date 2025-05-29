#!/usr/bin/env python3
"""
TPS测试代理服务器
用于处理CORS和转发请求到vLLM服务
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import logging

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/v1/chat/completions', methods=['POST', 'OPTIONS'])
def proxy_chat_completions():
    """代理聊天完成请求到vLLM服务"""
    if request.method == 'OPTIONS':
        # 处理预检请求
        return '', 204
    
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 获取目标URL（从请求头或后端类型）
        backend_type = request.headers.get('X-Backend-Type', 'vllm').lower()
        
        # 根据后端类型设置默认URL(使用各后端的标准默认端口)
        backend_urls = {
            'vllm': 'http://localhost:8000/v1/chat/completions',  # vLLM默认端口8000
            'sglang': 'http://localhost:30000/v1/chat/completions',  # SGLang默认REST API端口30000
            'ollama': 'http://localhost:11434/v1/chat/completions',  # Ollama默认端口11434
            'llama.cpp': 'http://localhost:8080/v1/chat/completions',  # llama.cpp server常见端口8080
            'mindie': 'http://localhost:5000/v1/chat/completions'  # Mindie常见端口5000
        }
        
        # 优先使用X-Target-URL头，否则根据后端类型选择URL
        target_url = request.headers.get('X-Target-URL', backend_urls.get(backend_type, backend_urls['vllm']))
        
        # 构建请求头
        headers = {
            'Content-Type': 'application/json'
        }
        
        # 如果有Authorization头，转发它
        auth_header = request.headers.get('Authorization')
        if auth_header:
            headers['Authorization'] = auth_header
        
        # 转发请求到vLLM服务
        logger.info(f"Forwarding request to: {target_url}")
        logger.info(f"Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(
            target_url,
            json=data,
            headers=headers,
            timeout=60  # 60秒超时
        )
        
        # 返回响应
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return jsonify({
            'error': {
                'message': f'Failed to connect to vLLM service: {str(e)}',
                'type': 'connection_error'
            }
        }), 503
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': {
                'message': f'Internal server error: {str(e)}',
                'type': 'internal_error'
            }
        }), 500

@app.route('/v1/models', methods=['GET'])
def proxy_models_list():
    """获取模型列表"""
    try:
        # 获取目标URL（从请求头或后端类型）
        backend_type = request.headers.get('X-Backend-Type', 'vllm').lower()
        
        # 根据后端类型设置默认URL(使用各后端的标准默认端口)
        backend_urls = {
            'vllm': 'http://localhost:8000/v1/models',  # vLLM默认端口8000
            'sglang': 'http://localhost:30000/v1/models',  # SGLang默认REST API端口30000
            'ollama': 'http://localhost:11434/v1/models',  # Ollama默认端口11434
            'llama.cpp': 'http://localhost:8080/v1/models',  # llama.cpp server常见端口8080
            'mindie': 'http://localhost:5000/v1/models'  # Mindie常见端口5000
        }
        
        # 优先使用X-Target-URL头，否则根据后端类型选择URL
        target_url = request.headers.get('X-Target-URL', backend_urls.get(backend_type, backend_urls['vllm']))
        
        # 构建请求头
        headers = {
            'Content-Type': 'application/json'
        }
        
        # 如果有Authorization头，转发它
        auth_header = request.headers.get('Authorization')
        if auth_header:
            headers['Authorization'] = auth_header
        
        # 转发请求到vLLM服务
        logger.info(f"Forwarding models request to: {target_url}")
        response = requests.get(target_url, headers=headers, timeout=10)
        
        # 返回响应
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Models request error: {str(e)}")
        return jsonify({
            'error': {
                'message': f'Failed to get models list: {str(e)}',
                'type': 'connection_error'
            }
        }), 503
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': {
                'message': f'Internal server error: {str(e)}',
                'type': 'internal_error'
            }
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    print("TPS测试代理服务器启动中...")
    print("默认监听地址: http://localhost:5000")
    print("使用方法: 将TPS测试页面的API URL设置为 http://localhost:5000/v1")
    print("支持的后端类型: vllm, sglang, ollama, llama.cpp, mindie")
    print("使用方法: 设置X-Backend-Type头指定后端类型")
    print("或使用X-Target-URL头直接指定目标URL")
    print("\n按 Ctrl+C 停止服务器")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
