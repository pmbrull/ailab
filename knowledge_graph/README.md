# Knowledge Graph

Build a knowledge graph with the following tools:
- BentoML service API to publish an API that serves embeddings
- Custom Neo4J to store the knowledge graph & embedding
- BentoML service API to publish the LLM Chatbot

## Embeddings API

- Run in test with `bentoml serve embeddings/embeddings_api:transformer`
- Test it with 
    ```bash
    curl -X POST "http://localhost:3000/embed" -H "Content-Type: application/json" --data '{"text": "What is the capital of France?"}'
    ```
- Build it with:
    ```bash
    make build
    ```
- Get the latest built version with `bentoml get transformer:latest -o json | jq ".version"`

## Neo4J Custom Embeddings

- Custom Neo4J APOC to have our own Cypher function calling the embeddings API
- Build and test locally with `mvn install`
