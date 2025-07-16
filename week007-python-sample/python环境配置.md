## pip源配置

```sh
mkdir ~/.pip
vim ~/.pip/pip.conf

pip install update
```

## HuggingFace配置
- 配置
```sh
pip install -U huggingface_hub hf_transfer -i https://pypi.tuna.tsinghua.edu.cn/simple
export HF_ENDPOINT=https://hf-mirror.com
```
- 下载模型
```sh
# 下载指定模型 & 下载到指定目录
huggingface-cli download Qwen/Qwen2.5-VL-32B-Instruct --local-dir /home/w30006808/models

# 端点续传
huggingface-cli download --resume-download Qwen/Qwen2.5-VL-32B-Instruct --local-dir /home/w30006808/models --resume

# 下载指定模型文件
huggingface-cli download --resume-download Qwen/Qwen2.5-VL-32B-Instruct tokenizer_config.json --local-dir /home/w30006808/models --resume
```

## pytorch配置
```sh
# 系统CUDA版本
nvcc --version

# 检查PyTorch版本
python -c "import torch; print(torch.__version__)"

# 检查CUDA版本
python -c "import torch; print(torch.version.cuda)"
```