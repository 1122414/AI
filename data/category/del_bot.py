import json
import os

# 文件路径
base_dir = r"E:\GitHub\Repositories\AI\data\labeled\chai"
tg_path = os.path.join(base_dir, "tg.json")
bot_path = os.path.join(base_dir, "bot.json")

# 关键词列表（可自行扩展）
keywords = [
    "请点击下面按钮认证你是真人",
    "广告合作、受骗举报上黑榜、请联系"
]

# 读取 tg.json
with open(tg_path, "r", encoding="utf-8") as f:
    tg_data = json.load(f)

bot_data = []
filtered_data = []

# 判断 content 是否包含任意关键词
for item in tg_data:
    if not isinstance(item, dict):
        continue
    content = str(item.get("content", ""))
    if any(kw in content for kw in keywords):
        bot_data.append(item)
    else:
        filtered_data.append(item)

# 若 bot.json 已存在，则追加写入
if os.path.exists(bot_path):
    with open(bot_path, "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
            if isinstance(existing_data, list):
                bot_data = existing_data + bot_data
        except json.JSONDecodeError:
            pass

# 保存结果
with open(bot_path, "w", encoding="utf-8") as f:
    json.dump(bot_data, f, ensure_ascii=False, indent=2)

with open(tg_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"✅ 处理完成！")
print(f"已将 {len(bot_data)} 条包含关键词的记录转移到 bot.json。")
print(f"tg.json 清理完成，剩余 {len(filtered_data)} 条数据。")
