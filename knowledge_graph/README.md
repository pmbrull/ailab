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