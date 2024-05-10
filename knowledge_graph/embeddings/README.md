# Embeddings API

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
