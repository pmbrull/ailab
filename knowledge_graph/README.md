# Knowledge Graph

Build a knowledge graph with the following tools:
- BentoML service API to publish an API that serves embeddings
- Custom Neo4J to store the knowledge graph & embedding
- BentoML service API to publish the LLM Chatbot

## Langchain example
- https://learn.deeplearning.ai/courses/knowledge-graphs-rag/lesson/8/chatting-with-the-knowledge-graph
Use the https://haystack.deepset.ai/integrations/neo4j-document-store dynamic document retriever + the LLM to
generate the best cypher query first?

## Memgraph

Run this from Memgraph Lab UI

```cypher
create user neo4j IDENTIFIED by 'neo4jneo4j';
```

- database `memgraph`

How do work with the vector indexes in memgraph?

Microchip webinar https://app.livestorm.co/memgraph/microchip-optimizes-chatbot-llm-queries-with-a-memgraph-knowledge-graph/live?s=7e4424a3-a69c-46cd-a67a-e7a27294a566#/chat
- We can even have an Agent that decides the "chain" -> generate SQL vs. search


- Custom LLM https://python.langchain.com/v0.1/docs/modules/model_io/llms/custom_llm/
- Memgraph Community Call w/ Brett Brewer - https://www.youtube.com/watch?v=okmk357t9W8
- LangChain has added Cypher Search - https://towardsdatascience.com/langchain-has-added-cypher-search-cb9d821120d5
- LangChain Cypher Search: Tips & Tricks - https://medium.com/neo4j/langchain-cypher-search-tips-tricks-f7c9e9abca4d
- Prompt Engineering Guide - https://www.promptingguide.ai/
- Building a Backend for ODIN and RUNE: How to Make a Knowledge Extraction Engine: https://memgraph.com/blog/building-backend-odin-rune-knowledge-extraction-engine
- Cosine Similarity https://memgraph.com/blog/cosine-similarity-python-scikit-learn
  - Chroma DB? https://github.com/chroma-core/chroma
- Query Agent? https://github.com/memgraph/bor/blob/main/core/knowledgebase/QueryAgents.py
- Text Search https://memgraph.com/docs/configuration/text-search


1. We can create embeddings to all our nodes https://memgraph.com/docs/advanced-algorithms/available-algorithms/node2vec
    ```cypher
    CALL node2vec.set_embeddings(True, 2.0, 0.5, 4, 5, 384) 
    YIELD nodes, embeddings
    RETURN nodes, embeddings;
    ```

Review this implementation? https://python.langchain.com/v0.1/docs/integrations/vectorstores/neo4jvector/
Example in Neo4J Haystack https://github.com/prosto/neo4j-haystack/blob/main/examples/rag_pipeline.py
- Neo4j implementation https://github.com/prosto/neo4j-haystack/blob/main/src/neo4j_haystack/document_stores/neo4j_store.py#L70

https://github.com/BaranziniLab/KG_RAG

## Just use Postgres?

https://christophergs.com/blog/production-rag-with-postgres-vector-store-open-source-models
RDS supports pgvector https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html#postgresql-extensions-16x
- pg_vector https://news.ycombinator.com/item?id=39613669
- RAG openAI https://chatgpt.com/share/435a3855-bf02-4791-97b3-4531b8e925ec?oai-dm=1
https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html#postgresql-extensions-16x 
- https://medium.com/@amodwrites/the-future-of-genai-with-kg-enhanced-rag-systems-c34928427453
- https://python.langchain.com/v0.1/docs/integrations/memory/postgres_chat_message_history/ to store chat history 

## RAG

https://newsletter.pragmaticengineer.com/p/rag & https://github.com/wordsmith-ai/hello-wordsmith
