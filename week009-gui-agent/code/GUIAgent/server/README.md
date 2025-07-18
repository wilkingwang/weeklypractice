# 一、ADB环境准备
## 1.1、下载ADB工具https://adb.clockworkmod.com/
## 1.2、开启调试模式
- 开启开发者模式
<div align=center><img src="./images/Development_Mode.png" alt="test" width="300" height="600"></div>

- 开启USB调试
<div align=center><img src="./images/Development_Option.png" alt="test" width="300" height="600"><img src="./images/Development_Option_USB.png" alt="test" width="300" height="600">></div>

- 查看设别

```sh
adb.exe devices
```

# 二、Python ADB
## 1、

## 2、

## 3、

## 4、

# 三、OmniParse部署
## 1、流程参考https://github.com/microsoft/OmniParser

## 2、下载模型
```sh
for f in icon_detect/{train_args.yaml,model.pt,model.yaml} icon_caption/{config.json,generation_config.json,model.safetensors}; do huggingface-cli download microsoft/OmniParser-v2.0 "$f" --local-dir weights; done
   mv weights/icon_caption weights/icon_caption_florence
```

## 3、启动服务
```sh
python -m omniparserserver --som_model_path ./weights/icon_detect/model.pt --caption_model_name florence2 --caption_model_path ./weights/icon_caption_florence --device cuda --BOX_TRESHOLD 0.05 --port 8080 --host 0.0.0.0
```

# 三、存在的问题
## 1、'adb' 不是内部或外部命令，也不是可运行的程序
解决方法：将adb.exe添加到PATH

## 2、vscode输出中文乱码
解决方法：python -X utf-8 test.py