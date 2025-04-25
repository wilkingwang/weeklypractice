### 一、GPTCache初始化
&ensp;&ensp;&ensp;&ensp;GPTCache核心组件包括：
- pre-process func
- embedding
- data manager
  - cache store
  - vector store
  - object store(optional, multi-mode)
- similarity evaluation
- post-process func

&ensp;&ensp;&ensp;&ensp;上面这些核心组件都需要在语义缓存初始化的时候设置，当然，大部分都有默认值。除这些参数外，还有其他参数，包括：

- config：缓存的一些其他配置，包括相似度阈值、某些特定预处理函数的参数值等。
- next-cache：可以用来设置多级缓存。例如，有两个GPTCache L1和L2，其中L1在初始化时将L2设置为下一个缓存。当收到用户请求时，如果L1缓存没有命中，会在L2缓存中查找；如果L2依然没有命中，则会调用LLM，并将结果保存到L1和L2缓存中；如果L2命中，则会将结果保存到L1中。

&ensp;&ensp;&ensp;&ensp;缓存的初始化目前有三种方法，分别时：
- 通过Cache的init方法，默认时精确匹配（简单的map cache），例如
```python
def init(
    self,
    cache_enable_func=cache_all,
    pre_func=last_content,
    embedding_func=string_embedding,
    data_manager: DataManager = get_data_manager(),
    similarity_evaluation=ExactMatchEvaluation(),
    post_func=temperature_softmax,
    config=Config(),
    next_cache=None,
  ):
  pass
```
- 使用api包中默认的`init_similar_cache `方法初始化语义匹配（onnx+sqlite+faiss）
```python
def init_similar_cache(
    data_dir: str = "api_cache",
    cache_obj: Optional[Cache] = None,
    pre_func: Callable = get_prompt,
    embedding: Optional[BaseEmbedding] = None,
    data_manager: Optional[DataManager] = None,
    evaluation: Optional[SimilarityEvaluation] = None,
    post_func: Callable = temperature_softmax,
    config: Config = Config(),
  ):
  pass
```
- 使用api包的`init_similar_cache_from_config`方法通过yaml配置文件初始化默认的模糊匹配（onnx+sqlite+faiss）
```python
def init_similar_cache_from_config(config_dir: str, cache_obj: Optional[Cache] = None):
  pass
```

#### 1.1、pre-process func
&ensp;&ensp;&ensp;&ensp;预处理函数主要用于从用户llm请求参数列表中获取用户问题信息，并将这部分信息组装成字符串返回。返回值时嵌入模型的输入。

&ensp;&ensp;&ensp;&ensp;值得注意的时，不同的llm需要使用不同的预处理函数，因为每个llm的请求参数列表是不一致的。并且包含用户问题信息的参数也是不同的。

&ensp;&ensp;&ensp;&ensp;当然，如果想根据用户的其他llm参数使用不同的预处理过程，也是可以的。

&ensp;&ensp;&ensp;&ensp;预处理函数的定义接收两个参数，返回值可以是一个或两个。
```python
def foo_pre_process_func(data: Dict[str, Any], **params: Dict[str, Any]) -> Any:
    pass
```
- 入参
  - data：用户参数
  - params：额外参数，例如cache配置文件，可以通过`params.get("cache_config", None)`获取。
- 出参
  - 如果没有特殊需求，函数可以返回一个值，用于embedding的输入和当前请求缓存的key。
  - 也可以返回两个值，第一个作为当前请求缓存的key，第二个作为embedding的输入，主要作用用于处理openai聊天对话。在长对话的情况下，第一个返回值是用户原始的长对话，只做了简单的对话字符串拼接，第二个返回值是通过一些模型提取长对话的关键信息，缩短了embeddeding输入。
#### 1.2、embedding
&ensp;&ensp;&ensp;&ensp;将输入转换为数字的多维数组，数字根据输入类型进行分类。

&ensp;&ensp;&ensp;&ensp;无论缓存是否准确，embedding model的选择更为重要。需要注意的几点：

- 模型支持的语言
- 模型支持的token数量
- 一般情况下，大的模型更准确，但耗时更长，小模型更快，但准确型较差

&ensp;&ensp;&ensp;&ensp;所有embedding模型包括：

- 文本
  - Onnx：最大支持512 token，仅支持英文
  - HuggingFace，默认是Distilbert-base-uncased，中文有uer/albert-base-chinese-cluecorpussmall
  - SBERT
  - OpenAI：openai api server
  - Cohere：copere api server
  - LangChain：langchain embedding model
  - Rwkv
  - PaddleNLP
  - UForm
  - FastText
- 语音
  - Data2VecAudio
- 图像
  - Timm
  - ViT
#### 1.3、Data Manager
&ensp;&ensp;&ensp;&ensp;对于文本的语义缓存，只需要cache store和vector store。如果是多模态缓存，还需要object store。存储的选择与llm无关，但需要注意的是，使用vector store时需要设置向量维度。

- cache store
  - sqlite
  - duckdb
  - mysql
  - mariadb
  - sqlserver
  - oracle
  - postgresql
- vector store
  - milvus
  - faiss
  - chromadb
  - hnswlib
  - pyvector
  - docarry
  - usearch
  - redis
- object store
  - local
  - s3

&ensp;&ensp;&ensp;&ensp;如何获取data manager：
- 根据store name，使用manager_factory获取
```python
from gptcache.manager import manager_factory

data_manager = manager_factory("sqlite,faiss", data_dir="./workspace", scalar_params={}, vector_params={"dimension": 128})
```
- 通过get_data_manager方法合并每个store对象
```python
from gptcache.manager import get_data_manager, CacheBase, VectorBase

data_manager = get_data_manager(CacheBase('sqlite'), VectorBase('faiss', dimension=128))
```
#### 1.4、Similarity Evaluation
&ensp;&ensp;&ensp;&ensp;如果想让缓存发挥更好的作用，除了embedding和vector engine，适当的相似度评估也是非常关键的。
&ensp;&ensp;&ensp;&ensp;相似度评估主要是：根据当前用户的llm请求，对回调缓存数据进行评估，得到一个浮点值。以下是已经存在的类似评估组件：

- SearchDistanceEvaluation：矢量搜索距离，简单、快速，但不是很准确
- OnnxModelEvaluation：使用模型来比较两个问题的关联程度，模型只支持512 token，比距离更精确
- NumpyNormEvaluation：计算llm请求的两个embedding向量与缓存数据之间的距离，快速简单，精度和距离几乎相同
- KReciprocalEvaluation：使用K-reprocical算法计算相似度进行重排序，并召回多个缓存数据进行比对。需要多次召回，这样比较耗时，相对来说更准确。
- CohereRerankEvaluation：使用cohere rerank api服务器
- SequenceMatchEvaluation：序列匹配，适用于多轮对话，将每轮对话分开进行相似评价，然后通过比例得到最终得分
- TimeEvaluation：按缓存创建时间进行评估，避免使用陈旧缓存
- SbertCrossencoderEvaluation：使用sbert模型进行重排序评估，这是目前发现的最好相似度评估
#### 1.5、post-process func
&ensp;&ensp;&ensp;&ensp;后处理主要是根据所有符合相似度阈值的缓存数据，得到用户问题的最终答案。可以在缓存数据列表中按照一定的策略选择其中一个，也可以使用模型对这些答案进行微调，是的相似的问题可以有不同的答案。
&ensp;&ensp;&ensp;&ensp;当前已有的后处理函数：
- tempreature_softmax：根据softmax策略进行选择，可以保证得到的缓存答案具有一定的随机性
- first：获取最相似的缓存答案
- random：获取随机一个
### 二、

https://gptcache.readthedocs.io/en/latest/configure_it.html

https://github.com/zilliztech/GPTCache/blob/main/docs/usage.md
https://github.com/zilliztech/GPTCache/blob/main/docs/feature.md
https://github.com/zilliztech/GPTCache/blob/main/examples/README.md
https://github.com/zilliztech/GPTCache/blob/main/docs/horizontal-scaling-usage.md