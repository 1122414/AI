#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
format_to_qa.py

把像下面这种原始记录（可能是 JSON array 或 JSON lines）：
{
  "name": "...",
  "description": "...",
  "label.name": [...],
  ...
}
或
{
  "content": "...",
  "label.name": [...],
  ...
}

转换为目标格式：
[
  {
    "instruction": "...",
    "input": "...",
    "output": "...",
    "system": "你现在是一个辨别黑灰产类别并将其进行实体分类的智能助手"
  },
  ...
]

用法:
python format_to_qa.py --input raw.json --output formatted.json
"""
import argparse
import json
import os
from typing import List, Dict, Any

SYSTEM_TEXT = "你现在是一个辨别黑灰产类别并将其进行实体分类的智能助手"

def read_input(path: str) -> List[Dict[str, Any]]:
    text = open(path, "r", encoding="utf-8").read().strip()
    if not text:
        return []
    # 尝试解析为 JSON array
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            # 单个对象，包成列表
            return [data]
    except json.JSONDecodeError:
        # 不是完整 JSON，尝试按行解析（JSONL）
        objs = []
        for i, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                objs.append(json.loads(line))
            except json.JSONDecodeError:
                # 跳过无法解析的行，但打印警告
                print(f"Warning: line {i} is not valid JSON and will be skipped.")
        return objs
    # 如果到这里仍未返回，返回空
    return []

def build_output_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    # 决定 instruction 的来源：description > content > name
    instruction = ""
    for key in ("description", "content", "name"):
        if key in rec and rec.get(key) not in (None, ""):
            # 如果是列表/对象，序列化为字符串；一般是字符串直接取
            val = rec.get(key)
            if not isinstance(val, str):
                instruction = json.dumps(val, ensure_ascii=False)
            else:
                instruction = val
            break

    # Build output: 聚合标签与行业字段
    label_fields = {}
    for k in rec:
        if k.startswith("label.") or k.startswith("industry."):
            label_fields[k] = rec[k]
    # output 必填：如果没有标签，则设置为空字符串
    output = ""
    if label_fields:
        output = json.dumps(label_fields, ensure_ascii=False)

    # Build input: 把原始记录中除 instruction 字段和标签/industry 字段之外的其余字段输出成字符串（可选）
    input_fields = {}
    # which key we used for instruction - determine its original key name
    instr_key = None
    for k in ("description", "content", "name"):
        if k in rec and rec.get(k) not in (None, ""):
            instr_key = k
            break

    for k, v in rec.items():
        if k == instr_key:
            continue
        if k.startswith("label.") or k.startswith("industry."):
            continue
        # 保留所有其他字段（包括原始 name, description if not used,地址等）
        input_fields[k] = v

    input_str = ""
    if input_fields:
        input_str = json.dumps(input_fields, ensure_ascii=False)

    # 如果 instruction 为空（极少数情况），尝试从 name 或 content 强制取值（宽容处理）
    if not instruction:
        instruction = rec.get("name") or rec.get("content") or ""

    return {
        "instruction": instruction,
        "input": input_str,
        "output": output,
        "system": SYSTEM_TEXT
    }

def main():
    parser = argparse.ArgumentParser(description="格式化原始记录到 QA JSON 结构")
    parser.add_argument("--input", "-i", required=True, help="输入文件（JSON array 或 JSONL）")
    parser.add_argument("--output", "-o", required=True, help="输出文件（JSON array）")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file {args.input} not found.")
        return

    records = read_input(args.input)
    if not records:
        print("No valid records found in input.")
        # 仍然写入空数组
        with open(args.output, "w", encoding="utf-8") as fo:
            json.dump([], fo, ensure_ascii=False, indent=2)
        print(f"Wrote empty array to {args.output}")
        return

    out_list = []
    for idx, r in enumerate(records, 1):
        try:
            out_rec = build_output_record(r)
            out_list.append(out_rec)
        except Exception as e:
            print(f"Warning: failed to process record #{idx}: {e}")

    # 写入输出文件
    with open(args.output, "w", encoding="utf-8") as fo:
        json.dump(out_list, fo, ensure_ascii=False, indent=2)

    print(f"Converted {len(out_list)} records -> {args.output}")

if __name__ == "__main__":
    main()
