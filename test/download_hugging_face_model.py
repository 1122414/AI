from huggingface_hub import snapshot_download

# 下载到本地路径，比如 G:/models/Qwen
model_dir = snapshot_download(
    repo_id="Qwen/Qwen2.5-1.5B-Instruct",
    local_dir="G:/models/Qwen/Qwen2.5-1.5B-Instruct"
)

print("模型已下载到:", model_dir)
