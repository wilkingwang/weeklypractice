### 一、语义匹配原理

### 二、语义匹配涉及技术

### 三、GPTCache原理
&ensp;&ensp;&ensp;&ensp;GPTCache利用在线服务的数据局部性特点，存储常用数据，降低检索时间，减轻后端服务器负载。与传统缓存系统不同，GPTCache进行语义缓存，识别存储相似或相关的查询以提高命中率。
&ensp;&ensp;&ensp;&ensp;GPTCache Adapter大语言模型适配器将大语言模型请求转换为缓存协议，并将缓存结果转为LLm响应。适配器目前支持api调用（put、get）、langchain、OpenAI等。以下内容以api调用为例：
#### 3.1、精准匹配缓存
##### 3.1.1、数据容器
&ensp;&ensp;&ensp;&ensp;精确匹配数据存储使用MAPDataManager，通过参数data_path、max_size和get_data_container参数来管理数据。

1、初始化
&ensp;&ensp;&ensp;&ensp;使用cachetools.LRUCache，初始化时通过pickle.load方法将缓存文件中的内容读出。
<div align=center><img src="map_data_manager_init.png"></div>
2、查找
<div align=center><img src="map_data_manager_get_scalar_data.png"></div>
3、保存
<div align=center><img src="map_data_manager_save.png"></div>

##### 3.1.2、初始化
1、参数

- cache_enable_func：函数用来给出是否启用缓存，默认时cache_all
- pre_embedding_func：提取特征向量之前的预处理，必须设置为get_prompt
- embedding_func：提取文本特征向量的方法：
- data_manager：缓存管理的DataManager
- similarity_evaluation：缓存命中后的评估方法
- post_process_messages_func：后处理，默认是temperature_softmax
- config：配置文件
- next_cache：

2、流程
<div align=center><img src="standard_cache_init.png"></div>
##### 3.1.3、put

1、参数

- prompt：缓存key
- data：缓存value
- kwargs：其他未定义的参数

2、流程

- pre_embedding_func提取特征向量之前的预处理，精准匹配缓存使用get_prompt，获取用户cache key
<div align=center><img src="standard_cache_pre_embedding_func.png"></div>
- embedding_func提取文本特征向量，精确匹配缓存使用string_embedding，获取用户embedding vector
<div align=center><img src="standard_cache_embedding_func.png"></div>
- 模拟llm请求
<div align=center><img src="standard_cache_llm_handle.png"></div>
- 缓存保存并刷新文件
<div align=center><img src="standard_cache_save.png"></div>
##### 3.1.4、get

#### 3.2、语义匹配缓存
##### 3.2.1、数据容器
&ensp;&ensp;&ensp;&ensp;语义匹配数据存储使用SSDataManager，通过参数cache_base、vector_base、max_size、clean_size、eviction参数类管理数据。
##### 3.2.1、初始化

##### 3.2.2、put

##### 3.2.3、get