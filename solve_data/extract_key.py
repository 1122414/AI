import json

def extract_keys_from_json(json_data):
    """
    从JSON数据中提取所有键
    :param json_data: JSON数据（字典或列表）
    :return: 所有键的集合
    """
    keys = set()
    
    def recurse(data):
        if isinstance(data, dict):
            for key, value in data.items():
                keys.add(key)
                recurse(value)
        elif isinstance(data, list):
            for item in data:
                recurse(item)
    
    recurse(json_data)
    return keys

def read_json_file(file_path):
    """
    从文件中读取JSON数据
    :param file_path: 文件路径
    :return: JSON数据
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取第一行数据作为示例
            first_line = file.readline().strip()
            if first_line:
                return json.loads(first_line)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    return None

def main():
    # JSON数据（示例数据）
    sample_data = {
        "platform": "0day.today", 
        "uuid": "149197ea2e6a00a46232bd698bab52ac", 
        "gather_time": "2025-03-18 18:32:46", 
        "domain": "sq542reyqwagfkghieehykb6hh6ohku5irarrrbeeo5iyozdbhe5n3id.onion", 
        "id": "[ 0Day-ID-39821 ]", 
        "name": "Akuvox Smart Intercom/Doorphone ServicesHTTPAPI Improper Access Control Vulnerability", 
        "description": "The Akuvox Smart Intercom/Doorphone suffers from an insecure service API access control. The vulnerability in ServicesHTTPAPI endpoint allows users with \"User\" privileges to modify API access settings and configurations. This improper access control permits privilege escalation, enabling unauthorized access to administrative functionalities. Exploitation of this issue could compromise system integrity and lead to unauthorized system modifications.", 
        "images": [], 
        "category_1": "web applications", 
        "category_2": ["web applications"], 
        "view_cnt": "830", 
        "buyer": "", 
        "comment_cnt": "0", 
        "address": "", 
        "update_time": "2025-03-18 18:32:46", 
        "net_type": "tor", 
        "price": 0, 
        "publish_time": "2024-11-27 08:00:00", 
        "sku": "0", 
        "sold_cnt": "0", 
        "url": "http://sq542reyqwagfkghieehykb6hh6ohku5irarrrbeeo5iyozdbhe5n3id.onion/exploit/description/39821", 
        "user_id": "b43363a19cdf3d3af35980e1e5f6e71e", 
        "user_name": "LiquidWorm", 
        "language": "en", 
        "label.name": ["安全漏洞"], 
        "label.keywords": [["vulnerability"]], 
        "industry.name": [], 
        "industry.keywords": [], 
        "region.country": [], 
        "region.province": [], 
        "region.city": [], 
        "identity": "{}", 
        "threaten_level": "low", 
        "area": "", 
        "comment_content": "[]"
    }
    
    # 提取键
    keys = extract_keys_from_json(sample_data)
    
    # 输出所有键
    print("JSON数据中的所有键:")
    for key in sorted(keys):
        print(f"  {key}")
    
    print(f"\n总共找到 {len(keys)} 个不同的键")
    
    # 如果需要从文件读取数据，可以使用以下代码：
    # file_path = "../data/test/test_data.json"
    # json_data = read_json_file(file_path)
    # if json_data:
    #     keys = extract_keys_from_json(json_data)
    #     print("从文件中提取的键:")
    #     for key in sorted(keys):
    #         print(f"  {key}")

if __name__ == "__main__":
    main()