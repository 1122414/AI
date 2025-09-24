from openai import OpenAI

client = OpenAI(
    base_url="http://172.23.216.104:5000/v1",
    api_key="sk-xxx",  # 随便填写，只是为了通过接口参数校验
)

completion = client.chat.completions.create(
    model="Qwen3-14b-chat",
    messages=[
        {"role": "user", "content": "现在我有一批暗网数据，请帮我对他们进行分类"}
    ]
)

print(completion.choices[0].message)

# import requests

# url = "http://172.23.216.104:5000/generate"
# data = {"prompt": '''你是谁'''}

# resp = requests.post(url, json=data)
# print(resp.text)
# print(resp.text.split(("\\n", 1)[1]))
