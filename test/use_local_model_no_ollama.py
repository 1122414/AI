import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# print(torch.cuda.is_available())
# print(torch.version.cuda)

model_name = "G:/models/Qwen/Qwen2.5-1.5B-Instruct"

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# 加载模型（低显存可以用 load_in_8bit / 4bit）
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    trust_remote_code=True,
    load_in_8bit=True
)

# 推理
inputs = tokenizer("写一首关于秋天的诗", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
