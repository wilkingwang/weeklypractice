import requests

try:
    rsp = requests.post(url="http://127.0.0.1:8000/hello")
    print(rsp)
except Exception as e:
    print(f"http req error: {str(e)}")
