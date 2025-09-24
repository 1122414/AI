import json
import random
import os

def read_json_data(file_path):
    """
    读取JSON文件中的数据
    :param file_path: JSON文件路径
    :return: 数据列表
    """
    data_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 每行是一个独立的JSON对象
                data = json.loads(line.strip())
                data_list.append(data)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    
    return data_list

def display_data_summary(data_list):
    """
    显示数据摘要
    :param data_list: 数据列表
    """
    print(f"总共读取到 {len(data_list)} 条记录")
    print("\n前3条记录的简要信息:")
    for i, data in enumerate(data_list[:3]):
        print(f"\n记录 {i+1}:")
        print(f"  平台: {data.get('platform', 'N/A')}")
        print(f"  名称: {data.get('name', 'N/A')}")
        print(f"  描述: {data.get('description', 'N/A')[:100]}..." if len(data.get('description', '')) > 100 else f"  描述: {data.get('description', 'N/A')}")
        labels = data.get('label.name', [])
        print(f"  类别: {', '.join(labels) if labels else 'N/A'}")

def save_category_data(data_list, category_name, count=1000):
    """
    保存指定类别的数据到JSON文件
    :param data_list: 数据列表
    :param category_name: 类别名称
    :param count: 保存的数据条数
    """
    # 筛选指定类别的数据
    category_data = []
    for data in data_list:
        labels = data.get('label.name', [])
        # 如果labels是字符串而不是列表，转换为列表
        if isinstance(labels, str):
            labels = [labels]
        # 如果数据包含指定类别，则添加到列表中
        if category_name in labels:
            category_data.append(data)
    
    # 如果该类别的数据不足count条，则抽取全部
    sample_count = min(count, len(category_data))
    
    # 随机抽取数据
    sampled_data = random.sample(category_data, sample_count)
    
    # 保存到文件
    filename = f"{category_name}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sampled_data, f, ensure_ascii=False, indent=2)
    
    print(f"  已保存 {sample_count} 条'{category_name}'类别的数据到 {filename}")

def main():
    # JSON文件路径
    json_file_path = r"E:\GitHub\Repositories\AI\data\test\tg_message_data.json"
    
    # 读取数据
    data_list = read_json_data(json_file_path)
    
    # 显示数据摘要
    if data_list:
        display_data_summary(data_list)
        
        # 示例: 查找特定平台的数据
        print("\n\n查找平台为'0day.today'的记录:")
        zero_day_data = [data for data in data_list if data.get('platform') == '0day.today']
        print(f"找到 {len(zero_day_data)} 条相关记录")
        
        # 示例: 按威胁等级分类
        print("\n\n按威胁等级统计:")
        threat_levels = {}
        for data in data_list:
            level = data.get('threaten_level', 'unknown')
            threat_levels[level] = threat_levels.get(level, 0) + 1
        
        for level, count in threat_levels.items():
            print(f"  {level}: {count} 条记录")
        
        # 按类别统计
        print("\n\n按类别统计:")
        categories = {}
        for data in data_list:
            labels = data.get('label.name', [])
            # 如果labels是字符串而不是列表，转换为列表
            if isinstance(labels, str):
                labels = [labels]
            # 统计每个类别
            for label in labels:
                categories[label] = categories.get(label, 0) + 1
        
        # 按数量排序并显示
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        print("\n按数量排序的类别:")
        for category, count in sorted_categories:
            print(f"  {category}: {count} 条记录")
        
        # 选择前四个类别并随机抽取数据
        print("\n\n从前四个类别中各随机抽取1000条数据:")
        top_categories = sorted_categories[:6]
        for category, count in top_categories:
            save_category_data(data_list, category, 1000)

if __name__ == "__main__":
    main()