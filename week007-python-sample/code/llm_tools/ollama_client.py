import requests
import time

def main():
    messages = [{
        "role": "user",
        "content": "who are you"
    }]

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen2.5vl:72b",
        "messages": messages,
        "stream": False
    }

    response = requests.post("http://159.138.231.181:11434/api/chat", json=data, headers=headers)
    rsp = response.json()
    print(rsp)


if __name__ == '__main__':
    for i in range(0, 1000000):
        main()
        time.sleep(3)
        