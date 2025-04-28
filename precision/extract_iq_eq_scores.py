import json
import csv
import os
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
                if os.path.exists(json_path):
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
                        
                        results.append({
                            'model_name': model_name,
                            'date': formatted_date,
                            'IQ_score': iq_score,
                            'EQ_score': eq_score
                        })
    
    # 写入CSV文件
    with open('model_scores.csv', 'w', newline='') as csvfile:
        fieldnames = ['model_name', 'date', 'IQ_score', 'EQ_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"成功处理{len(results)}条记录，结果已保存到model_scores.csv")

if __name__ == '__main__':
    process_reports()
