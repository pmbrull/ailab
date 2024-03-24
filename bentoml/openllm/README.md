# Building A Production-Ready LangChain Application with BentoML and OpenLLM

MacOS cannot have CUDA, since it comes from NVIDIA GPUs.

- [ref](https://www.bentoml.com/blog/building-a-production-ready-langchain-application-with-bentoml-and-openllm)

## Introduction

```bash
uv venv
source .venv/bin/activate
uv pip install langchain "openllm[mistral]"  # Does not work with `uv`
brew install tensorrt
```

Installation error

```
OSError: CUDA_HOME environment variable is not set. Please set it to your CUDA
install root
```

## Run the LLM

```
TRUST_REMOTE_CODE=True DTYPE=float32 openllm start mistralai/Mistral-7B-Instruct-v0.1 --backend pt
```
Fails on Macos

> Use vLLM for PROD -> requires CUDA

```
docker run --platform=linux/amd64 --rm -it -p 3000:3000 ghcr.io/bentoml/openllm start mistralai/Mistral-7B-Instruct-v0.1 --backend pt
docker run --platform=linux/amd64 --rm -it -p 3000:3000 ghcr.io/bentoml/openllm start facebook/opt-1.3b --backend vllm
```

Not working for now. Let's try https://github.com/ollama/ollama
1. Install `Ollama`
2. `ollama pull llama2`
3. `llm = Ollama(model="llama2")`

## For PROD

https://python.langchain.com/docs/integrations/llms/openllm

```
You may also choose to initialize an LLM managed by OpenLLM locally from
current process. This is useful for development purpose and allows developers
to quickly try out different types of LLMs.

When moving LLM applications to production, we recommend deploying the OpenLLM
server separately and access via the server_url option demonstrated above.
```

## Check GPU

```python
import psutil
import torch

ram = psutil.virtual_memory()
ram_total = ram.total / (1024**3)
print('MemTotal: %.2f GB' % ram_total)

print('=============GPU INFO=============')
if torch.cuda.is_available():
  !/opt/bin/nvidia-smi || ture
else:
  print('GPU NOT available')
```

## Expand to build a RAG

- https://www.packtpub.com/article-hub/build-your-first-rag-with-qdrant

run qdrant

```
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```
