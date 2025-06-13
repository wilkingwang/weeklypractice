import time
from openai import OpenAI

def main():
    client = OpenAI(
        base_url="http://159.138.231.181:8000/v1/",
        api_key="ollama"
    )

    chat_completion = client.chat.completions.create(
        model="qwen2.5vl:7b",
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
    for i in range(0, 1000000):
        main()
        time.sleep(3)