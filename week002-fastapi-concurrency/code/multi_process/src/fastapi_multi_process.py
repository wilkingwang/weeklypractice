import os
import sys
import uvicorn
from fastapi import FastAPI
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from src.config.config import Config

config = Config()

cfg = {}
cfg['host'] = config.get('endpoint')['host']
cfg['port'] = config.get('endpoint')['port']
cfg['workers'] = config.get('endpoint')['workers']

app = FastAPI()

@app.post("/hello")
def predict():
    return "Hello World."

if __name__ == "__main__":
    uvicorn.run(app="fastapi_multi_process:app", host=cfg['host'], port=cfg['port'], log_level="debug", workers=cfg['workers'])
