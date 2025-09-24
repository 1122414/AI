# import json
# import requests

# url = "http://localhost:11434/api/generate"
# prompt = "写一首关于秋天的诗"

# resp = requests.post(
#   url,
#   json={"model": "qwen3:8b", "prompt" : prompt},
#   stream=True
# )

# output = ""
# for part in resp.iter_lines():
#         if part:
#             try:
#                 piece = json.loads(part.decode("utf-8"))
#                 output += piece.get("response", "")
#             except json.JSONDecodeError:
#                 continue

# print(output.strip())

from ollama import chat, generate

response = generate(model="qwen3:8b", prompt="写一首关于秋天的诗")
print(response['response'])
