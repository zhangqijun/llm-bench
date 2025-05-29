import json
import csv
import os
import subprocess
import shutil
from datetime import datetime

def process_reports():
    results = []
    base_dir = 'outputs'
    
    # 遍历outputs目录
    for root, dirs, files in os.walk(base_dir):
        if 'reports' in dirs:
            reports_dir = os.path.join(root, 'reports')
            date_str = os.path.basename(root)  # 如20250424_170512
            
            # 尝试解析日期
            try:
                date_obj = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_date = date_str
            
            # 处理每个模型报告
            model_dirs = [d for d in os.listdir(reports_dir) 
                         if os.path.isdir(os.path.join(reports_dir, d))]
            
            for model_dir in model_dirs:
                json_path = os.path.join(reports_dir, model_dir, 'iquiz.json')
                # if not os.path.exists(json_path):
                #     shutil.rmtree(root)  # 删除整个日期目录
                #     break  # 跳出当前日期目录的处理循环
                
                with open(json_path, 'r') as f:
                        data = json.load(f)
                        
                        model_name = data['model_name']
                        iq_score = eq_score = 0
                        
                        # 提取IQ和EQ分数
                        for subset in data['metrics'][0]['categories'][0]['subsets']:
                            if subset['name'] == 'IQ':
                                iq_score = subset['score']
                            elif subset['name'] == 'EQ':
                                eq_score = subset['score']
                        
                        # 构建日志文件路径
                        log_path = os.path.join(root, 'logs', 'eval_log.log')
                        # 构建配置文件路径并读取api_url
                        config_path = None
                        api_url = 'null'
                        try:
                            import glob
                            import yaml
                            config_files = glob.glob(os.path.join(root, 'configs', 'task_config_*.yaml'))
                            if config_files:
                                config_path = config_files[0]  # 取第一个匹配的文件
                                with open(config_path, 'r') as f:
                                    config = yaml.safe_load(f)
                                    api_url = config.get('api_url', 'null')
                        except:
                            pass
                            
                        results.append({
                            'model_name': model_name,
                            'date': formatted_date,
                            'IQ_score': iq_score,
                            'EQ_score': eq_score,
                            'api_url': api_url
                        })
    
    # 按(model_name, api_url)分组，只保留每组的最新记录
    latest_results = {}
    for result in results:
        model_name = result['model_name']
        api_url = result['api_url']
        current_date = result['date']
        key = (model_name, api_url)
        
        # 如果模型+api组合不存在于字典中，或者当前日期更新，则更新记录
        if (key not in latest_results) or \
           (current_date > latest_results[key]['date']):
            latest_results[key] = result
    
    # 按IQ+EQ总分排序
    sorted_results = sorted(latest_results.values(), 
                          key=lambda x: x['IQ_score'] + x['EQ_score'], 
                          reverse=True)
    
    # 写入CSV文件
    with open('model_scores.csv', 'w', newline='') as csvfile:
        fieldnames = ['model_name', 'date', 'IQ_score', 'EQ_score', 'api_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_results)
    
    print(f"成功处理{len(results)}条记录，结果已保存到model_scores.csv")

if __name__ == '__main__':
    # 执行主流程
    process_reports()
