import json
import os

base_dir = r"E:\GitHub\Repositories\AI\data\labeled\chai"

# 文件路径
tg_input = os.path.join(base_dir, "tg.json")
tor_input = os.path.join(base_dir, "tor.json")
tg_output = os.path.join(base_dir, "tg_final.json")
tor_output = os.path.join(base_dir, "tor_final.json")

# 抽取字段定义
tg_fields = ["content", "label.name", "label.keywords", "industry.name", "industry.keywords"]
tor_fields = ["name", "description", "label.name", "label.keywords", "industry.name", "industry.keywords"]

def extract_field(data, field_path):
    """安全提取多级字段，如 'label.name'"""
    key = field_path
    value = data
    if isinstance(value, dict) and key in value:
        value = value[key]
    else:
        return None
    return value

def extract_data(input_path, fields):
    """从指定文件提取字段"""
    if not os.path.exists(input_path):
        print(f"⚠️ 文件不存在：{input_path}")
        return []
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 无法读取 {input_path}: {e}")
        return []

    result = []
    for item in data:
        if not isinstance(item, dict):
            continue
        new_item = {}
        for field in fields:
            new_item[field] = extract_field(item, field)
        result.append(new_item)
    return result

# 执行抽取
tg_final = extract_data(tg_input, tg_fields)
tor_final = extract_data(tor_input, tor_fields)

# 写入结果
with open(tg_output, "w", encoding="utf-8") as f:
    json.dump(tg_final, f, ensure_ascii=False, indent=2)

with open(tor_output, "w", encoding="utf-8") as f:
    json.dump(tor_final, f, ensure_ascii=False, indent=2)

print(f"✅ 处理完成！")
print(f"tg_final.json 已生成，共 {len(tg_final)} 条记录")
print(f"tor_final.json 已生成，共 {len(tor_final)} 条记录")
