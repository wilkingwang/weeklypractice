### 一、vllm介绍
&ensp;&ensp;vLLM是大语言模型高速推理框架，旨在极大地提高实时场景下的语言模型服务的吞吐与内存使用效率。其核心是PagedAttention技术，让KVCache不用再存储在一大块连续的空间中，解决了LLM服务中内存瓶颈问题。

&ensp;&ensp;从PagedAttention到连续批处理(Continous Batching)、CUDA Graph、模型量化(Quantization)、模型并行、前缀缓存(Prefix Caching)、推测解码(Speculative Decoding)等等一系列的技术，提高了LLM的推理速度和资源利用率。

&ensp;&ensp;vLLM的性能瓶颈主要是由阻塞GPU执行的CPU开销造成的。在vLLM v0.6中引入一系列优化，以减少此类开销。

### 二、vLLM参数配置

#### 1、tensor_parallel_size分布式推理
&ensp;&ensp;分布式推理是指在多个计算节点上并行执行推理任务的过程。
&ensp;&ensp;**单卡**:无分布式推理，至少两张显卡
&ensp;&ensp;**单台服务器多显卡(张量并行推理)**：当模型的规模超过了单个GPU的显存容量时，将模型的输入数据(张量)分割成多个小部分，每个GPU处理其中的一部分。如果服务器有4个GPU，可以将张良并行大小设置为4，这意味着模型将被分割成4部分，每个GPU处理其中一部分。
&ensp;&ensp;**多服务器多GPU(张量并行+流水线并行推理)**：张量并行是指将模型的参数（权重和激活）分割到不同的GPU上。流水线并行(层间并行)是指将模型的不同层分配到不同的节点上。每个节点负责模型的一部分层，数据在节点间流动，通过流水线的方式进行处理。张量并行大小是每个节点中使用的GPU数量，流水线并行大小是你想要使用的节点数量。

&ensp;&ensp;**补充：**tensor_parallel_size的值还和使用的大模型有关，否则会报错。大模型头数可以查看大模型config.json中的参数num_attention_heads。tensor_parallel_size参数需要能被部署的大模型的注意力头数整除。

#### 2、Quantization量化
&ensp;&ensp;量化是本地运行LLM的主要议题，因为它能较少内存占用。
&ensp;&ensp;vLLM支持多种类型的量化模型，例如AWQ、GPTQ、SqueezeLLM等，选择哪种量化方法确实需要根据模型来决定。
- AWQ：即激活值感知的权重量化
- GPTQ：针对类GPT LLM模型的量化方法
- GPTQ-Marlin：vLLM 0.6版本以后引入的特性，对GPTQ的一种优化实现，优选
#### 3、enforce-eager
&ensp;&ensp;*enforce-eager*是一个参数，用于控制vLLM是否始终使用PyTorch的eager(即时执行模式),默认为false，vLLM会默认使用eager模式和CUDA Graph的混合模式来执行操作，这种混合模式旨在提供最大的性能和灵活性。

&ensp;&ensp;CUDA Graph是PyTorch中用于优化性能的一种技术，金庸CUDA Graph可能会影响性能，但可以减少内存需求。对于小模型，CUDA Graph可能对性能提升有帮助，但对于大模型，性能差异可能不大。

#### 4、gpu-memory-utilization
&ensp;&ensp;gpu-memory-utilization用来控制GPU显存使用量的百分比。
&ensp;&ensp;如果设置的值过高，可能会导致GPU内存不足，影响模型的性能或者导致崩溃；如果设置的过低，可能会导致GPU内存没有得到充分利用，影响模型的运行效率。默认值为0.9。

#### 5、max-model-len
&ensp;&ensp;模型的上下文长度(Context Length)指模型在生成响应之前可以"回顾"和"理解"的输入内容的长度，是模型在处理输入时能够考虑的历史信息的总长度。通过max-model-len控制，不添加此参数时，系统将尝试使用最大可能的序列长度。配置要求如下：

- 小于模型本身的最大Position Embedding
&ensp;&ensp;单词的顺序通常包含重要的语义信息，位置嵌入(Position Embedding)是模型用来标记输入数据位置信息的，指定了模型在处理序列数据时能够考虑的最大位置数。例如Transformer架构，在输入的部分由文本的每个Token向量(Input Embedding)与每个Token的位置编码(Position Encoding)向量进行相加处理后的值在输入到每个Attention Block。

    <table>
        <tr>
            <td width=192>公司</td>
            <td width=192>模型</td>
            <td width=192>上下文长度</td>
        </tr>
        <tr>
            <td width=192>OpenAI</td>
            <td width=192>GPT-3.5<br>GPT-4</td>
            <td width=192>4k-16k<br>8k-32k</td>
        </tr>
        <tr>
            <td width=192>Anthropic</td>
            <td width=192>Claude<br>Claude2</td>
            <td width=192>100k<br>100k</td>
        </tr>
        <tr>
            <td width=192>Meta</td>
            <td width=192>LLAMA<br>LLAMA2<br>LLAMA2 Long</td>
            <td width=192>2k<br>4k<br>32k</td>
        </tr>
    </table>

- 显存需求
&ensp;&ensp;在某些情况下，可能会因为GPU内存限制而需要调整模型的最大序列长度(缩小输入长度，可能减少模型在处理序列时需要存储的Key-Value缓存的数据量，从而节省内存需求)。
&ensp;&ensp;上下文窗口变大，LLM需要更多的脑力和记忆空间来工作。这意味着成本也会增加。

- 输出长度控制
&ensp;&ensp;max-tokens指定了不全(completion)过程中模型可以生成的最大tokens数，这是模型输出的上限，即模型在生成回答或内容时，不会超过这个tokens数。
&ensp;&ensp;max-tokens设置多大合适：

    - 建议max-tokens设置小一点，因为在自然语言处理过程中，较长的文本输出通常需要更长的计算时间和更多的计算资源。
    - 不可以大于上下文长度。上下文长度限制了模型在任何给定时间点能够处理的信息总量，无论是输入还是输出。上下文长度=输入长度（包括prompt）+输出长度
    - 限制 max_tokens 能够增加 prompt 的长度，如 gpt-3.5-turbo 的限制为 4097 tokens，如果设置 max_tokens=4000，那么 prompt 就只剩下 97 tokens 可用，如果超过就会报错

#### 6、长系统提示enable_prefix_caching
&ensp;&ensp;系统通常会遇到相同的前缀。单论对话中system prompt是相同的，多轮对话中每一轮对话要依赖历史对话，对它们的KV Cache进行缓存，就不用每次重新计算。

- **多轮对话：**在聊天机器人或客服系统中，前缀缓存可以显著优化性能
- **长系统提示：**在需要长系统提示的场景中，前缀缓存可以减少Prefill阶段的计算开销
- **高并发请求：**在处理大量重复前缀的请求时，前缀缓存可以提高系统的吞吐量

&ensp;&ensp;enable_prefix_caching=True 表示启用前缀缓存（Prefix Caching）功能。该功能通过缓存已计算的键值对（KV Cache）来减少重复计算，从而提高推理效率。

#### 7、长序列输入use-v2-block-manager
&ensp;&ensp;KV缓存(Key-Value Cache)是存储中间计算结果的重要结构。在处理长序列时，传统的缓存管理方法可能会导致显存不足或推理延迟增加。这是因为长序列需要更大的缓存空间，而显存容量有限。

&ensp;&ensp;块管理器（BlockSpaceManager）负责管理 KV 缓存的索引，优化缓存的分配和使用，V2 版本的块管理器在性能和资源管理方面进行了改进。use-v2-block-manager用于启用 V2 版本的块管理器（BlockSpaceManagerV2）。V2块管理器支持动态调整缓存大小，根据输入序列的长度和实际需求灵活分配缓存资源。通过更高效的内存管理策略，减少内存碎片化，提高缓存的利用率。

- V2块管理器将长序列分割成多个小块，逐块处理并缓存
- 支持将部分缓存卸载到CPU内存中，从而扩展GPU的虚拟内存

#### 8、显存占用过高enable-chunked-prefill
&ensp;&ensp;在大语言模型中，当输入序列很长时，Prefill阶段的计算量会非常大，这会导致：

- 首次Token生成时间(TTFT)增加，即模型生成第一个Token的时间边长
- 显存占用过高，可能导致显存不足或推理效率下降

&ensp;&ensp;`enable-chunked-prefill`将长序列分解为多个块，每个块分别处理。这样可以减少单词prefill的计算量和显存占用，从而优化TTFT和显存使用效率。

&ensp;&ensp;GPT推理分为两个阶段：prefill阶段和decode阶段：

- **prefill：**是用户输入完prompt到生成首个Token的过程。将用户输入的文本(Prompt)分解为Token，然后计算对应的Key和Value向量，存储在KV缓存中。Prefill是计算密集型，GPU的利用率较高。
- **decode：**为生成首个Token到推理停止的过程，decode是存储密集型，GPU的利用率较低，IO消耗大。

&ensp;&ensp;可以通过设置`max_num_batched_tokens`参数来进一步优化。`max_num_batched_tokens`用于控制每次批处理中最大的Token数量。

- 对实时性要求较高：建议将`max_num_batched_tokens`设置为较小的值（如256-512）
- 需要处理大量请求：设置为较大的值（1024-4096），提高Prefill阶段的批处理能力，从而提高整体吞吐量
- 确保设置的值不超过GPU的显存容量，避免OOM

#### 9、加速推理speculative-mode="[ngram]"
&ensp;&ensp;通过并行化解码过程来提高LLM的推理效率，尤其是在生成较长文本时。

- Speculative Mode
&ensp;&ensp;投机掩码的核心思想是利用模型的预测能力，在生成当前Token的同时，提前预测并生成后续的多个Token。这些提前生成的Token成为"投机Token"。如果后续的实际生成与投机Token一致，则可以直接使用这些Token，从而减少等待时间；如果不一致，则丢弃并重新生成。

&ensp;&ensp;[ngram]是一种具体的投机解码策略，表示使用N-Gram并行解码，在生成当前Token的同时，提前生成后续的N个Token，这些Token是基于当前上下文并行生成的，而不是逐个生成。

&ensp;&ensp;生成较长文本时，逐个Token生成的效率很低。投机掩码可以提前生成多个Token，加快文本的生成速度。
- num_speculative_tokens
&ensp;&ensp;指定了每次并行生成的 Token 数量。例如，如果设置为 4，则模型会在生成当前 Token 的同时，提前并行生成后续的 4 个 Token。增加 num_speculative_tokens 会显著增加显存占用，尤其是在长序列生成任务中。一般不会设置的太大。
- use-v2-block-manager
&ensp;&ensp;投机解码需要与 V2 块管理器（--use-v2-block-manager）配合使用，因为 V2 块管理器支持更复杂的缓存管理策略。
- ngram_prompt_lookup_max
&ensp;&ensp;在投机解码过程中，用于提示查找（Prompt Lookup）的 n-gram 窗口的最大大小。

### 二、vllm模型创建


### 三、大模型推理指标
- TPS（Token Per Second）
&ensp;&ensp;每秒模型输出的token数量。