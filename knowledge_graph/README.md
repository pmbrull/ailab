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
    make build VERSION=0.0.1
    make push VERSION=0.0.1
    ```
- Get the latest built version with `bentoml get transformer:latest -o json | jq ".version"`

## Neo4J Custom Embeddings

- Custom Neo4J APOC to have our own Cypher function calling the embeddings API
- Build and test locally with `mvn install`
- Deployed in an image `neo-embedding`

From the neo4j pod we need to communicate to the transformed pod. We can test things out via:

```bash
kubectl exec -n knowledge-graph -it <neo4j pod> -- bash
# Then execute 
curl -X POST "http://transformer.knowledge-graph.svc.cluster.local:3000/embed" -H "Content-Type: application/json" --data '{"text": "What is the capital of France?"}'
```

From the neo4j pod we can also run the cypher shell and test out the custom function:

```bash
k -n knowledge-graph exec -it deployment/neo-embedding -- bash
cypher-shell
CALL io.ailab.embeddings('I am a random string') YIELD embedding RETURN embedding;
:exit
```

## Neo4J Vector Index

Python utils:

```python
from neo4j import GraphDatabase, RoutingControl

def cypher_read_query(query, **parameters):
    with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
        records, _, _ = driver.execute_query(
            query,
            parameters_=parameters,
            database_=NEO4J_DATABASE,
            routing_=RoutingControl.READ,
        )
        return records


def cypher_write_query(query, **parameters):
    with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
        result = driver.execute_query(
            query,
            parameters_=parameters,
            database_=NEO4J_DATABASE,
            routing_=RoutingControl.WRITE,
        )
        return result
```

1. Create the vector index with

```cypher
CREATE VECTOR INDEX movie_tagline_embeddings IF NOT EXISTS
  FOR (m:Movie) ON (m.taglineEmbedding) 
  OPTIONS { indexConfig: {
    `vector.dimensions`: 384,
    `vector.similarity_function`: 'cosine'
  }}
```

If we use the https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 model, dimension is 384.

TODO:
- update the dimensions for new models
- research better similarity functions

Notebooks:
- https://github.com/neo4j-examples/sec-edgar-notebooks/tree/main
- https://github.com/prosto/neo4j-haystack-playground/blob/main/neo4j_haystack_journey.ipynb


2. Add the embeddings

```cypher
MATCH (movie:Movie)
WHERE movie.tagline IS NOT NULL
CALL io.ailab.embeddings(movie.tagline) YIELD embedding
CALL db.create.setNodeVectorProperty(movie, 'embedding', embedding)
```

This will `setNodeVectorProperty` to the node `movie`, on a new field `embedding` with the `embedding` result
from our custom procedure `io.ailab.embeddings`.

3. Query similar movies using the vector tagline

```python
import httpx
import numpy as np

# Use the same transformer model
query_embedding = httpx.post("http://localhost:9891/embed", data={"text": "v for vendetta"})
query_embedding.json()

question_embedding = np.array(query_embedding.json().get("embedding"))

cypher_read_query("""
  CALL db.index.vector.queryNodes('movie-embeddings', $top_k, $embedding)
  YIELD node AS similarMovie, score

  MATCH (similarMovie) WHERE similarMovie.released > 2000
  RETURN similarMovie.title, similarMovie.tagline AS tagline, score
""", embedding=question_embedding, top_k=3)
```

## Clean Database

```cypher
match (a) -[r] -> () delete a, r;
match (a) delete a;
```

## Langchain example
- https://learn.deeplearning.ai/courses/knowledge-graphs-rag/lesson/8/chatting-with-the-knowledge-graph
Use the https://haystack.deepset.ai/integrations/neo4j-document-store dynamic document retriever + the LLM to
generate the best cypher query first?

