import os
import json

# 输入和输出路径
input_dir = r"E:\GitHub\Repositories\AI\data\labeled"
output_dir = os.path.join(input_dir, "chai")
os.makedirs(output_dir, exist_ok=True)

tg_path = os.path.join(output_dir, "tg.json")
tor_path = os.path.join(output_dir, "tor.json")

tg_data = []
tor_data = []

# 遍历所有文件
for root, _, files in os.walk(input_dir):
    for file in files:
        if not file.endswith(".json"):
            continue
        file_path = os.path.join(root, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ 无法解析文件 {file_path}: {e}")
            continue

        # 有些文件可能是列表形式
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    if "platform" in item:
                        tor_data.append(item)
                    else:
                        tg_data.append(item)
        elif isinstance(data, dict):
            if "platform" in item:
                tor_data.append(item)
            else:
                tg_data.append(item)

# 保存结果
with open(tg_path, "w", encoding="utf-8") as f:
    json.dump(tg_data, f, ensure_ascii=False, indent=2)

with open(tor_path, "w", encoding="utf-8") as f:
    json.dump(tor_data, f, ensure_ascii=False, indent=2)

print(f"✅ 处理完成！")
print(f"包含 id 的数据已保存到：{tg_path}")
print(f"包含 platform 的数据已保存到：{tor_path}")
