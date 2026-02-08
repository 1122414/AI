import json
import os

def format_data(input_path, output_path):
    formatted = []

    # 读取源文件
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        # ---------- Step 1. 构造输入内容 ----------
        # 情况1：有 name + description
        if "name" in item and "description" in item:
            input_text = f"name: {item['name']}\ndescription: {item['description']}"
        # 情况2：有 content
        elif "content" in item:
            input_text = item["content"]
        else:
            input_text = ""

        # ---------- Step 2. 构造输出内容 ----------
        # 去掉非标签内容，只保留label相关字段
        label_info = {}
        for key in item.keys():
            if key.startswith("label.") or key.startswith("industry."):
                label_info[key] = item[key]
        output_text = json.dumps(label_info, ensure_ascii=False)

        # ---------- Step 3. 拼接成目标格式 ----------
        formatted_item = {
            "instruction": "你现在是一个给黑灰产数据打标签分类的智能助手",
            "input": input_text,
            "output": output_text,
            "system": "你现在是一个辨别黑灰产类别并将其进行实体分类的智能助手"
        }

        formatted.append(formatted_item)

    # ---------- Step 4. 保存结果 ----------
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted, f, ensure_ascii=False, indent=2)

    print(f"✅ 格式化完成，输出文件: {output_path}, 共 {len(formatted)} 条数据。")


if __name__ == "__main__":
    # 示例：根据实际路径修改
    input_path = r"E:\GitHub\Repositories\AI\data\labeled\final_use\tor_final.json"
    output_path = r"E:\GitHub\Repositories\AI\data\labeled\llama_factory_data\llama_factory_data_tor_final.json"
    format_data(input_path, output_path)
