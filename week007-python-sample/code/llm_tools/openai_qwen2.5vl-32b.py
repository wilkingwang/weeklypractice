import os
import sys
import time
import yaml
from openai import OpenAI

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

if current_dir not in sys.path:
    sys.path.append(current_dir)

def main(base_url, model_name):
    client = OpenAI(
        base_url=base_url,
        api_key="ollama"
    )

    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': 'who are you'
                    }
                ]
            }
        ]
    )

    print(chat_completion.choices[0].message.content)

if __name__ == '__main__':
    with open ('./config/qwen2.5vl-32b.yaml', 'r') as f:
        config = yaml.load(f)

    print(config)
    print(config['api_url'], config['model_name'])
    for i in range(0, 1000000):
        main(config['api_url'], config['model_name'])
        time.sleep(3)