### 一、部署概念
&ensp;&ensp;&ensp;&ensp;在部署FastAPI应用程序或任何类型的Web API时，需要注意以下概念
#### 1.1、安全性
&ensp;&ensp;&ensp;&ensp;HTTPS通常由应用程序服务器的外部组件提供。并且必须有某个东西负责更新HTTPS证书。
#### 1.2、启动时运行
&ensp;&ensp;&ensp;&ensp;
#### 1.3、重新启动

#### 1.4、复制
- 多进程

&ensp;&ensp;&ensp;&ensp;如果您的客户端数量多于单个进程可以处理的数量，并且服务器的CPU中有多个核心，那么可以让多个进程同时处理一个应用程序，并在它们之间分发所有请求。

&ensp;&ensp;&ensp;&ensp;当运行同一程序的多个进程时，它们通常称为workers。
- 工作进程和端口

&ensp;&ensp;&ensp;&ensp;为了同时拥有多个进程，必须有一个单个进程监听端口，然后以某种方式将通信传输到每个工作进程。

- 进程内存
&ensp;&ensp;&ensp;&ensp;多个进程通常不共享任何内存。这意味着每个正在进行的进程都有自己的东西、变量和内存。

- 复制工具和策略
&ensp;&ensp;&ensp;&ensp;主要限制是必须有一个单个组件来处理公共IP中的端口。然后它必须有一种方法及那个通信传输到复制的进程/worker。以下是一些可能的组合和策略：

  - Gunicorn管理Uvicorn workers：Gunicorn将是监听IP和端口的进程管理器，复制将通过多个Uvicorn工作进程进行
  - Uvicorn管理Uvicorn workers：一个Uvicorn进程管理器将监听IP和端口，并且它将启动多个Uvicorn工作进程
  - Kubernetes和其他分布式容器系统：k8s层中某些组件将监听IP和端口。复制将通过拥有多个容器，每个容器运行一个Uvicorn进程

### 二、使用Uvicorn的多工作进程模式

&ensp;&ensp;&ensp;&ensp;部署应用程序时，如果希望进行进程复制，以利用多喝CPU并能够处理更多请求。
- fastapi run --worker 4 main.py
- uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4