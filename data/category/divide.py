import json
import os
import random

# 输入路径
base_dir = r"E:\GitHub\Repositories\AI\data\labeled\final_use"

# 输出路径
train_dir = r"E:\GitHub\Repositories\AI\data\labeled\train"
test_dir = r"E:\GitHub\Repositories\AI\data\labeled\test"

os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 需要划分的文件
files = ["tg_final.json", "tor_final.json"]

split_ratio = 0.3  # 测试集比例

for file_name in files:
    input_path = os.path.join(base_dir, file_name)
    if not os.path.exists(input_path):
        print(f"⚠️ 文件不存在：{input_path}")
        continue

    # 读取数据
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 随机划分
    random.shuffle(data)
    n_total = len(data)
    n_test = int(n_total * split_ratio)

    test_data = data[:n_test]
    train_data = data[n_test:]

    # 输出文件路径
    base_name = file_name.replace("_final.json", "")
    test_path = os.path.join(test_dir, f"{base_name}_test.json")
    train_path = os.path.join(train_dir, f"{base_name}_train.json")

    # 写入文件
    with open(test_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    with open(train_path, "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)

    print(f"✅ {file_name} 划分完成：")
    print(f"   总数 {n_total} 条 → 训练集 {len(train_data)} 条，测试集 {len(test_data)} 条")
    print(f"   📁 训练集保存到: {train_path}")
    print(f"   📁 测试集保存到: {test_path}")
