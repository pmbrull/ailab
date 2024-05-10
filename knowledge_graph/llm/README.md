# LLM 

- Run in test with `bentoml serve llm:LLM` or `make serve`
- Test it with 
    ```bash
    curl -X POST "http://localhost:3001/ask" -H "Content-Type: application/json" --data '{"query": "What is the capital of France?"}'
    ```
- Build it with:
    ```bash
    make build VERSION=0.0.1
    make push VERSION=0.0.1
    ```
- Get the latest built version with `bentoml get transformer:latest -o json | jq ".version"`
