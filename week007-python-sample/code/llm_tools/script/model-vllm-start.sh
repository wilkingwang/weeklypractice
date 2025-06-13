#!/bin/bash

cd /home/w30006808/models

# nohup python -m vllm.entrypoints.openai.api_server --model ./Qwen2.5-VL-32B-Instruct-AWQ/ --served-model-name qwen2.5vl:32b --max-model-len=32768 --tensor-parallel-size 1 --quantization awq --gpu-memory-utilization=0.9 --dtype float16 --enforce-eager --trust-remote-code --host 0.0.0.0 --port 8000 > qwen2.5-vl-32b.log 2>&1 &

conda_name="miniconda3"

if [ -d "~/anaconda3" ]; then
    conda_name="anaconda3"
fi

if [ $3 -eq 1 ]; then
    source ~/${conda_name}/etc/profile.d/conda.sh && source ~/${conda_name}/bin/activate vllm && nohup python -m vllm.entrypoints.openai.api_server --model $1 --served-model-name $2 --max-model-len=32768 --tensor-parallel-size 1 --quantization awq --gpu-memory-utilization=0.9 --dtype float16 --enforce-eager --trust-remote-code --host 0.0.0.0 --port $4 > qwen2.5-vl-32b.log 2>&1 &
else
    source ~/${conda_name}/etc/profile.d/conda.sh && source ~/${conda_name}/bin/activate vllm && nohup python -m vllm.entrypoints.openai.api_server --model $1 --served-model-name $2 --max-model-len=32768 --tensor-parallel-size 1 --gpu-memory-utilization=0.9 --dtype float16 --enforce-eager --trust-remote-code --host 0.0.0.0 --port $4 > qwen2.5-vl-32b.log 2>&1 &
fi
