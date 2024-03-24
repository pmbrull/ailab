# AI Lab

## LLM

- [LLM Architecture](https://github.blog/2023-10-30-the-architecture-of-todays-llm-applications/)
- [Serve LLMs as an API - RunGPT](https://github.com/jina-ai/rungpt)
- [How to Build a RAG System With LlamaIndex, OpenAI, and MongoDB Vector Database](https://www.mongodb.com/developer/products/atlas/rag-with-polm-stack-llamaindex-openai-mongodb/?user_id=65e9dd753de01c671b5b0fbd&sn_type=LINKEDIN&cpost_id=65f829cf6cb6022687b77ed9&post_id=12883905854&asset_id=ADVOCACY_205_65f2c86b41a2e13b870f23be)
- [Understanding LLMs](https://www.linkedin.com/pulse/understanding-llms-fine-tuning-vs-vector-databases-christopher-daden/)

  - Hallucination: **information limitation** of an LLM
  - Not aligned with used expectations: **behavioral limitation**
  - For example, a company might use **fine-tuning** to train a customer service bot to respond in a way that aligns with their brand's tone of voice, and then use a **vector database (embedding)** to provide the bot with access to their company policies and procedures.

- [Context Window](https://www.hopsworks.ai/dictionary/context-window-for-llms)

- [Orca outperforms GPT-4?](https://www.microsoft.com/en-us/research/project/orca/)

### Fine Tuning

- [LLM fine tuning](https://www.superannotate.com/blog/llm-fine-tuning)
- [OSS Fine tuning axolotl](https://github.com/OpenAccess-AI-Collective/axolotl)

### OpenAI

- [OpenAI Counting Tokens in Stream](https://news.ycombinator.com/item?id=39699917)

## MLOps

- [BentoML](https://www.bentoml.com/) - Deploy models as APIs
  - [Quickstart](https://docs.bentoml.com/en/latest/get-started/quickstart.html?_gl=1*1fqas9*_gcl_au*MTM2MTE1NzEzMi4xNzExMjIxMjgx)

### BentoML

- [Easily deploy models as APIs](https://docs.bentoml.com/en/latest/guides/services.html)
- [Containerize models and deploy them as images](https://docs.bentoml.com/en/latest/guides/containerization.html)
- [Guide on testing services](https://docs.bentoml.com/en/latest/guides/testing.html)
- [Deploy as ASGI Server](https://docs.bentoml.com/en/latest/guides/asgi.html)

With LLM

- [Serve LLMs](https://docs.bentoml.com/en/latest/use-cases/large-language-models/vllm.html) using `vLLM`, a high-throughput and memory-efficient inference and serving engine for LLMs

CICD

- [GitHub Actions](https://docs.bentoml.com/en/v1.1.11/guides/github-actions.html)
- [Store and use custom private models models](https://docs.bentoml.org/en/latest/guides/model-store.html) - Build the model, store in S3, use it anywhere as a Service after downloading:
  - With the Python Client `bentoml.models.import_model('s3://my_bucket/folder/my_model.bentomodel')`

### BentoML - OpenLLM

- [OpenLLM](https://github.com/bentoml/OpenLLM) - Operating LLMs in production
- [Building A Production-Ready LangChain Application with BentoML and OpenLLM](https://www.bentoml.com/blog/building-a-production-ready-langchain-application-with-bentoml-and-openllm)

## Vector Database

Vector embeddings serve as a bridge between the raw textual input and the language model’s neural network.

- [What are Vector DBs?](https://qdrant.tech/articles/what-is-a-vector-database/)
- [What are Vector Embeddings?](https://qdrant.tech/articles/what-are-embeddings/)
- [Choosing the Right Embedding Model: A Guide for LLM Applications](docs/Choosing the Right Embedding Model: A Guide for LLM Applications | by Ryan Nguyen | Medium.pdf)
- [Transformers Architecture](https://arxiv.org/abs/1706.03762)
- [Evaluate RAG Responses](https://superlinked.com/vectorhub/evaluating-retrieval-augmented-generation-a-framework-for-assessment)

### Qdrant

- [Build a FAQ Chat](https://qdrant.tech/articles/faq-question-answering/)
- [Qdrant embedding Mistral](https://qdrant.tech/documentation/embeddings/mistral/)
- [Build your first RAG](https://www.packtpub.com/article-hub/build-your-first-rag-with-qdrant)
- [RAG Systems Architecture](https://qdrant.tech/articles/what-is-rag-in-ai/#)
- [From HuggingFace dataset to Qdrant vector database in 12 minutes flat](https://www.gptechblog.com/from-huggingface-dataset-to-qdrant-vector-database-in-12-minutes-flat/)

## Hugging Face

- [Learn how to build an advanced chatbot with a cloud vector database](https://gurjeet333.medium.com/learn-how-to-build-a-chatbot-from-scratch-on-a-free-cloud-vector-database-193a7fa29c13)
- [Creating a simple chatbot with open-source LLMs using Python and Hugging Face](https://medium.com/@danushidk507/creating-a-simple-chatbot-with-open-source-llms-using-python-and-hugging-face-01a9f5a7ebdf)

## Langchain

- [Introduction](https://python.langchain.com/docs/get_started/introduction)
- [Building an LLM open source search engine in 100 lines using LangChain and Ray](https://www.anyscale.com/blog/llm-open-source-search-engine-langchain-ray)
