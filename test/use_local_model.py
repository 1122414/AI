import json
import requests
import re
from typing import List, Dict, Any, Union


def extract_json(text: str) -> Dict[str, Any]:
    """
    从模型输出中提取 JSON 部分，如果没有则返回 {"label": 原始文本}
    """
    matches = re.findall(r"\{.*?\}", text, re.DOTALL)
    if matches:
        last_json = matches[-1]  # 取最后一个 JSON
        try:
            return json.loads(last_json)
        except json.JSONDecodeError:
            return {"label": last_json}
    return {"label": text.strip()}


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """
    读取 JSON 文件，支持 JSON 数组和 JSONL/NDJSON 格式
    """
    items = []
    with open(file_path, "r", encoding="utf-8") as f:
        first_char = f.read(1)
        f.seek(0)
        if first_char == "[":  # JSON 数组
            try:
                items = json.load(f)
            except json.JSONDecodeError as e:
                print("JSON数组解析失败:", e)
        else:  # JSONL/NDJSON
            for line in f:
                if line.strip():
                    try:
                        items.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print("JSONL解析失败:", e, "内容:", line[:100])
    return items


def call_qwen(prompt: str, model: str = "qwen3:8b") -> str:
    """
    调用本地 Ollama Qwen 模型，获取响应文本（合并流式返回）
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt},
        stream=True
    )

    output = ""
    for part in response.iter_lines():
        if part:
            try:
                piece = json.loads(part.decode("utf-8"))
                output += piece.get("response", "")
            except json.JSONDecodeError:
                continue
    return output.strip()


def tag_json_with_qwen(json_file: str, model: str = "qwen3:8b", output_file: str = "tagged.json"):
    data = load_json_data(json_file)
    results = []

    for i, item in enumerate(data, 1):
        if '点击下方按钮' in item['content']:
          print(f"[{i}/{len(data)}] 正在处理 id={item.get('id', 'N/A')} 标准人机，跳过...")
          continue
        prompt = f"请阅读下面的 JSON 数据，\n{json.dumps(item, ensure_ascii=False)} \n\n它是Telegram——“飞机”软件中的一句句对话的形式，你从中辨别黑灰产对话，并给它打上具体黑灰产类别的标签。注意：1.非黑灰产对话则返回{{\"label\": \"正常对话\"}}；2.其中会包含机器人发言，比如：Gijg，15 秒内点击下方按钮以获得发言的权限👇🏻等，则返回{{\"label\": \"人机发言\"}}；3.黑灰产标内容返回你判断的具体黑灰产分类：只输出以下的JSON格式：{{\"label\": \"色情内容、数据泄露、走私贩毒、电信诈骗\"}}，注意label需要你自己根据信息判断，而不是直接填写上述例子中的label"

        print(f"[{i}/{len(data)}] 正在处理 id={item.get('id', 'N/A')} ...")

        label_output = call_qwen(prompt, model=model)
        label_json = extract_json(label_output)

        item["label"] = label_json.get("label", "未识别")
        results.append(item)

    # 保存结果为 JSONL
    with open(output_file, "w", encoding="utf-8") as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ 打标签完成，已保存到 {output_file}")


if __name__ == "__main__":
    tag_json_with_qwen(r"E:\GitHub\Repositories\AI\data\test\tg_message_data.json")
