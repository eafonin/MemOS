---
source_url: https://memos-docs.openmem.net/open_source/modules/memories/kv_cache_memory
section: Memories
scraped_date: 2025-10-16
title: KVCacheMemory: Key-Value Cache for Activation Memory
has_images: no
has_tables: yes
---

# KVCacheMemory: Key-Value Cache for Activation Memory
 [ `KVCacheMemory` is a specialized memory module in MemOS for storing and managing key-value (KV) caches, primarily used to accelerate large language model (LLM) inference and support efficient context reuse. It is especially useful for activation memory in conversational and generative AI systems. 
## KV-cache Memory Use Cases
 
[In MemOS, KV-cache memory is best suited for storing **semantically stable and frequently reused background content** such as:]
 
- [Frequently asked questions (FAQs) or domain-specific knowledge]
- [Prior conversation history]
 
[These stable **plaintext memory items** are automatically identified and managed by the `MemScheduler` module. Once selected, they are converted into KV-format representations (`KVCacheItem`) ahead of time. This precomputation step stores the activation states (Key/Value tensors) of the memory in a reusable format, allowing them to be injected into the modelâs attention cache during inference.]
 
[Once converted, these KV memories can be **reused across queries without requiring re-encoding** of the original content. This reduces the computational overhead of processing and storing large amounts of text, making it ideal for applications that require **rapid response times** and **high throughput**.]
 
## Why KV-cache Memory
 
[Integrating `MemScheduler` with KV-cache memory enables significant performance optimization, particularly in the **prefill phase** of LLM inference.]
 
### Without KVCacheMemory
 
- [Each new query is appended to the full prompt, including the background memory.]
- [The model must **recompute token embeddings and attention** over the full sequence â even for unchanged memory.]
 
### With KVCacheMemory
 
- [The background content is **cached once** as Key/Value tensors.]
- [For each query, only the new user input (query tokens) is encoded.]
- [The previously cached KV is injected directly into the attention mechanism.]
 
### Benefits
 
[This separation reduces redundant computation in the prefill phase and leads to:]
 
- [Skipping repeated encoding of background content]
- [Faster attention computation between query tokens and cached memory]
- [**Lower Time To First Token (TTFT)** latency during generation]
 
[This optimization is especially valuable in:]
 
- [Multi-turn chatbot interactions]
- [Retrieval-augmented or context-augmented generation (RAG, CAG)]
- [Assistants operating over fixed documentation or FAQ-style memory]
 
### KVCacheMemory Acceleration Evaluation
 
[To validate the performance impact of KV-based memory injection, we conducted a set of controlled experiments simulating real memory reuse in MemOS.]
 
#### Experiment Setup
 
[During typical usage, the `MemScheduler` module continuously tracks interaction patterns and promotes high-frequency, stable plaintext memory into KV format. These KV memories are loaded into GPU memory as activation caches and reused during inference.]
 
[The evaluation compares two memory injection strategies:]
 
1. [**Prompt-based injection**: background memory is prepended as raw text.]
2. [**KV-cache injection**: memory is injected directly into the modelâs attention cache.]
 
[We test these strategies across:]
 
- [**Three context sizes**: short, medium, and long]
- [**Three query types**: short-form, medium-form, and long-form]
 
[The primary metric is **Time To First Token (TTFT)**, a key latency indicator for responsive generation.]
 
#### Results
 
[The following table shows results across three models (Qwen3-8B, Qwen3-32B, Qwen2.5-72B). TTFT under KV-cache injection is consistently lower than prompt-based injection, while the output tokens remain identical across both strategies.] `Build (s)` refers to the one-time preprocessing cost of converting the memory to KV format, amortized across multiple queries. <table><thead><tr><th>Model</th><th>Ctx</th><th>CtxTok</th><th>Qry</th><th>QryTok</th><th>Build (s)</th><th>KV TTFT (s)</th><th>Dir TTFT (s)</th><th>Speedup (%)</th></tr></thead><tbody><tr><td>Qwen3-8B</td><td>long</td><td>6064</td><td>long</td><td>952.7</td><td>0.92</td><td>0.50</td><td>2.37</td><td>79.1</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>0.93</td><td>0.19</td><td>2.16</td><td>91.1</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>0.93</td><td>0.12</td><td>2.04</td><td>94.2</td></tr><tr><td></td><td>medium</td><td>2773</td><td>long</td><td>952.7</td><td>0.41</td><td>0.43</td><td>1.22</td><td>64.6</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>0.41</td><td>0.16</td><td>1.08</td><td>85.1</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>0.43</td><td>0.10</td><td>0.95</td><td>89.7</td></tr><tr><td></td><td>short</td><td>583</td><td>long</td><td>952.7</td><td>0.12</td><td>0.39</td><td>0.51</td><td>23.0</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>0.12</td><td>0.14</td><td>0.32</td><td>55.6</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>0.12</td><td>0.08</td><td>0.29</td><td>71.3</td></tr><tr><td>Qwen3-32B</td><td>long</td><td>6064</td><td>long</td><td>952.7</td><td>0.71</td><td>0.31</td><td>1.09</td><td>71.4</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>0.71</td><td>0.15</td><td>0.98</td><td>84.3</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>0.71</td><td>0.11</td><td>0.96</td><td>88.8</td></tr><tr><td></td><td>medium</td><td>2773</td><td>long</td><td>952.7</td><td>0.31</td><td>0.24</td><td>0.56</td><td>56.9</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>0.31</td><td>0.12</td><td>0.47</td><td>75.1</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>0.31</td><td>0.08</td><td>0.44</td><td>81.2</td></tr><tr><td></td><td>short</td><td>583</td><td>long</td><td>952.7</td><td>0.09</td><td>0.20</td><td>0.24</td><td>18.6</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>0.09</td><td>0.09</td><td>0.15</td><td>39.6</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>0.09</td><td>0.07</td><td>0.14</td><td>53.5</td></tr><tr><td>Qwen2.5-72B</td><td>long</td><td>6064</td><td>long</td><td>952.7</td><td>1.26</td><td>0.48</td><td>2.04</td><td>76.4</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>1.26</td><td>0.23</td><td>1.82</td><td>87.2</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>1.27</td><td>0.15</td><td>1.79</td><td>91.4</td></tr><tr><td></td><td>medium</td><td>2773</td><td>long</td><td>952.7</td><td>0.58</td><td>0.39</td><td>1.05</td><td>62.7</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>0.58</td><td>0.18</td><td>0.89</td><td>79.2</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>0.71</td><td>0.23</td><td>0.82</td><td>71.6</td></tr><tr><td></td><td>short</td><td>583</td><td>long</td><td>952.7</td><td>0.16</td><td>0.33</td><td>0.43</td><td>23.8</td></tr><tr><td></td><td></td><td></td><td>medium</td><td>302.7</td><td>0.16</td><td>0.15</td><td>0.27</td><td>43.2</td></tr><tr><td></td><td></td><td></td><td>short</td><td>167</td><td>0.16</td><td>0.10</td><td>0.25</td><td>60.5</td></tr></tbody></table>
 
#### vLLM-based Performance
 
[MemOS now supports using vLLM to manage activation memory. To evaluate the impact of KV Cache prefilling for different prefix text lengths, we conducted performance tests on a system equipped with 8x `H800 80GB GPUs (112 vCPUs, 1920 GiB Memory)` and a system equipped with 8x `RTX4090-24G-PCIe (112 vCPUs, 960 GiB Memory)`. The evaluation covered two core models: Qwen3-32B and Qwen2.5-72B.]
 
[The benchmarks were run across a range of memory and context length combinations to simulate various activation memory scenarios:]
 
- [**Memory Text Lengths (tokens)**: 500, 1000, 2000]
- [**Context Text Lengths (tokens)**: 500, 1000, 2000, 4000]
 
[The following table summarizes the benchmark results.]
 
[**Qwen2.5-72B**]
 
- [On 4090 (2 Nodes 16 GPUs)]
 
<table><thead><tr><th>mem tks</th><th>prompt tks</th><th>TTFT (without cache, ms)</th><th>TTFT (With cache, ms)</th><th>TTFT Speedup (%)</th><th>Abs Dis(ms)</th></tr></thead><tbody><tr><td>0.5k</td><td>0.5k</td><td>1787.21</td><td>851.47</td><td>52.358%</td><td>935.74</td></tr><tr><td>0.5k</td><td>1k</td><td>2506.26</td><td>1290.68</td><td>48.502%</td><td>1215.58</td></tr><tr><td>0.5k</td><td>2k</td><td>3843.48</td><td>2897.97</td><td>24.600%</td><td>945.51</td></tr><tr><td>0.5k</td><td>4k</td><td>6078.01</td><td>5200.86</td><td>14.432%</td><td>877.15</td></tr><tr><td>1k</td><td>0.5k</td><td>2274.61</td><td>920.16</td><td>59.546%</td><td>1354.45</td></tr><tr><td>1k</td><td>1k</td><td>2907.17</td><td>1407.65</td><td>51.580%</td><td>1499.52</td></tr><tr><td>1k</td><td>2k</td><td>4278.53</td><td>2916.47</td><td>31.835%</td><td>1362.06</td></tr><tr><td>1k</td><td>4k</td><td>6897.99</td><td>5218.94</td><td>24.341%</td><td>1679.05</td></tr><tr><td>2k</td><td>0.5k</td><td>3460.12</td><td>782.73</td><td>77.379%</td><td>2677.39</td></tr><tr><td>2k</td><td>1k</td><td>4443.34</td><td>1491.24</td><td>66.439%</td><td>2952.10</td></tr><tr><td>2k</td><td>2k</td><td>5733.14</td><td>2758.48</td><td>51.885%</td><td>2974.66</td></tr><tr><td>2k</td><td>4k</td><td>8152.76</td><td>5627.41</td><td>30.975%</td><td>2525.35</td></tr></tbody></table>
 
- [On H800 (4 GPUs)]
 
<table><thead><tr><th>mem tks</th><th>prompt tks</th><th>TTFT (without cache, ms)</th><th>TTFT (With cache, ms)</th><th>TTFT Speedup (%)</th><th>Abs Dis(ms)</th></tr></thead><tbody><tr><td>0.5k</td><td>0.5k</td><td>51.65</td><td>52.17</td><td>-1.007%</td><td>-0.52</td></tr><tr><td>0.5k</td><td>1k</td><td>55.70</td><td>57.03</td><td>-2.388%</td><td>-1.33</td></tr><tr><td>0.5k</td><td>2k</td><td>74.23</td><td>78.56</td><td>-5.833%</td><td>-4.33</td></tr><tr><td>0.5k</td><td>4k</td><td>77.56</td><td>77.45</td><td>0.142%</td><td>0.11</td></tr><tr><td>1k</td><td>0.5k</td><td>55.90</td><td>55.73</td><td>0.304%</td><td>0.17</td></tr><tr><td>1k</td><td>1k</td><td>55.35</td><td>52.89</td><td>4.444%</td><td>2.46</td></tr><tr><td>1k</td><td>2k</td><td>80.14</td><td>73.82</td><td>7.886%</td><td>6.32</td></tr><tr><td>1k</td><td>4k</td><td>82.83</td><td>73.51</td><td>11.252%</td><td>9.32</td></tr><tr><td>2k</td><td>0.5k</td><td>75.82</td><td>71.31</td><td>5.948%</td><td>4.51</td></tr><tr><td>2k</td><td>1k</td><td>80.60</td><td>78.71</td><td>2.345%</td><td>1.89</td></tr><tr><td>2k</td><td>2k</td><td>83.91</td><td>78.60</td><td>6.328%</td><td>5.31</td></tr><tr><td>2k</td><td>4k</td><td>99.15</td><td>80.12</td><td>19.193%</td><td>19.03</td></tr></tbody></table>
 
[**Qwen3-32B**]
 
- [On 4090 (1 Nodes 8 GPUs)]
 
<table><thead><tr><th>mem tks</th><th>prompt tks</th><th>TTFT (without cache, ms)</th><th>TTFT (With cache, ms)</th><th>TTFT Speedup (%)</th><th>Abs Dis(ms)</th></tr></thead><tbody><tr><td>0.5k</td><td>0.5k</td><td>288.72</td><td>139.29</td><td>51.756%</td><td>149.43</td></tr><tr><td>0.5k</td><td>1k</td><td>428.72</td><td>245.85</td><td>42.655%</td><td>182.87</td></tr><tr><td>0.5k</td><td>2k</td><td>683.65</td><td>538.59</td><td>21.218%</td><td>145.06</td></tr><tr><td>0.5k</td><td>4k</td><td>1170.48</td><td>986.94</td><td>15.681%</td><td>183.54</td></tr><tr><td>1k</td><td>0.5k</td><td>409.83</td><td>137.96</td><td>66.337%</td><td>271.87</td></tr><tr><td>1k</td><td>1k</td><td>507.95</td><td>262.21</td><td>48.379%</td><td>245.74</td></tr><tr><td>1k</td><td>2k</td><td>743.48</td><td>539.71</td><td>27.408%</td><td>203.77</td></tr><tr><td>1k</td><td>4k</td><td>1325.34</td><td>1038.59</td><td>21.636%</td><td>286.75</td></tr><tr><td>2k</td><td>0.5k</td><td>686.01</td><td>147.34</td><td>78.522%</td><td>538.67</td></tr><tr><td>2k</td><td>1k</td><td>762.96</td><td>246.22</td><td>67.728%</td><td>516.74</td></tr><tr><td>2k</td><td>2k</td><td>1083.93</td><td>498.05</td><td>54.051%</td><td>585.88</td></tr><tr><td>2k</td><td>4k</td><td>1435.39</td><td>1053.31</td><td>26.619%</td><td>382.08</td></tr></tbody></table>
 
- [On H800 (2 GPUs)]
 
<table><thead><tr><th>mem tks</th><th>prompt tks</th><th>TTFT (without cache, ms)</th><th>TTFT (With cache, ms)</th><th>TTFT Speedup (%)</th><th>Abs Dis(ms)</th></tr></thead><tbody><tr><td>0.5k</td><td>0.5k</td><td>161.18</td><td>97.61</td><td>39.440%</td><td>63.57</td></tr><tr><td>0.5k</td><td>1k</td><td>164.00</td><td>121.39</td><td>25.982%</td><td>42.61</td></tr><tr><td>0.5k</td><td>2k</td><td>257.34</td><td>215.20</td><td>16.375%</td><td>42.14</td></tr><tr><td>0.5k</td><td>4k</td><td>365.14</td><td>317.95</td><td>12.924%</td><td>47.19</td></tr><tr><td>1k</td><td>0.5k</td><td>169.45</td><td>100.52</td><td>40.679%</td><td>68.93</td></tr><tr><td>1k</td><td>1k</td><td>180.91</td><td>128.25</td><td>29.108%</td><td>52.66</td></tr><tr><td>1k</td><td>2k</td><td>271.69</td><td>210.00</td><td>22.706%</td><td>61.69</td></tr><tr><td>1k</td><td>4k</td><td>389.30</td><td>314.64</td><td>19.178%</td><td>74.66</td></tr><tr><td>2k</td><td>0.5k</td><td>251.43</td><td>130.92</td><td>47.930%</td><td>120.51</td></tr><tr><td>2k</td><td>1k</td><td>275.81</td><td>159.60</td><td>42.134%</td><td>116.21</td></tr><tr><td>2k</td><td>2k</td><td>331.11</td><td>218.17</td><td>34.110%</td><td>112.94</td></tr><tr><td>2k</td><td>4k</td><td>451.06</td><td>334.80</td><td>25.775%</td><td>116.26</td></tr></tbody></table>
 
[The results clearly demonstrate that integrating vLLM's KV Cache reuse provides a transformative performance improvement for MemOS.]
 
## KV-cache Memory Structure
 
[KV-based memory reuse via `KVCacheMemory` offers substantial latency reduction across model sizes and query types, while maintaining identical output. By shifting reusable memory from plaintext prompts into precomputed KV caches, MemOS eliminates redundant context encoding and achieves faster response timesâespecially beneficial in real-time, memory-augmented LLM applications.]
 
[Each cache is stored as a `KVCacheItem`:]
 
<table><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>kv_cache_id</td><td>str</td><td>Unique ID for the cache (UUID)</td></tr><tr><td>kv_cache</td><td>DynamicCache</td><td>The actual key-value cache (transformers)</td></tr><tr><td>metadata</td><td>dict</td><td>Metadata (source, extraction time, etc.)</td></tr></tbody></table>
 
## API Summary (KVCacheMemory)
 
### Initialization
 
```
KVCacheMemory(config: KVCacheMemoryConfig)

```
 
### Core Methods
 
<table><thead><tr><th>Method</th><th>Description</th></tr></thead><tbody><tr><td>extract(text)</td><td>Extracts a KV cache from input text using the LLM</td></tr><tr><td>add(memories)</td><td>Adds one or more KVCacheItem to memory</td></tr><tr><td>get(memory_id)</td><td>Fetch a single cache by ID</td></tr><tr><td>get_by_ids(ids)</td><td>Fetch multiple caches by IDs</td></tr><tr><td>get_all()</td><td>Returns all stored caches</td></tr><tr><td>get_cache(cache_ids)</td><td>Merge and return a combined cache from multiple IDs</td></tr><tr><td>delete(ids)</td><td>Delete caches by IDs</td></tr><tr><td>delete_all()</td><td>Delete all caches</td></tr><tr><td>dump(dir)</td><td>Serialize all caches to a pickle file in directory</td></tr><tr><td>load(dir)</td><td>Load caches from a pickle file in directory</td></tr><tr><td>from_textual_memory(mem)</td><td>Convert a TextualMemoryItem to a KVCacheItem</td></tr><tr><td>build_vllm_kv_cache( messages)</td><td>Build a vLLM KV cache from a list of messages</td></tr></tbody></table>
 
[When calling `dump(dir)`, the system writes to:]
 
```
/

```
 
[This file contains a pickled dictionary of all KV caches, which can be reloaded using `load(dir)`.]
 
## How to Use
 
```
from memos.configs.memory import KVCacheMemoryConfig
from memos.memories.activation.kv import KVCacheMemory

config = KVCacheMemoryConfig(
 extractor_llm={
 "backend": "huggingface",
 "config": {"model_name_or_path": "Qwen/Qwen3-1.7B"}
 }
)
mem = KVCacheMemory(config)

# Extract and add a cache
cache_item = mem.extract("The capital of France is Paris.")
mem.add([cache_item])

# Retrieve and merge caches
merged_cache = mem.get_cache([cache_item.kv_cache_id])

# Save/load
mem.dump("tmp/act_mem")
mem.load("tmp/act_mem")

```
 
## Developer Notes
 
- [Uses HuggingFace `DynamicCache` for efficient key-value storage]
- [Pickle-based serialization for fast load/save]
- [All methods are covered by integration tests in `/tests`]
