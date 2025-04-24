import time
import uvicorn
from src.config.config import Config
from threading import Lock
from fastapi import FastAPI, HTTPException

config = Config()

cfg = {}
config['host'] = cfg.get('endpoint')['host']
config['port'] = cfg.get('endpoint')['port']

app = FastAPI()

@app.post("/hello")
def predict():
    return "Hello World."

if __name__ == "__main__":
    uvicorn.run(app="fastapi_multi_process:app", host=config['host'], port=config['port'], log_level="debug")