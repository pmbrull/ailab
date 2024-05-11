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


- quantization requires GPU? https://stackoverflow.com/questions/76924239/accelerate-and-bitsandbytes-is-needed-to-install-but-i-did
- llama.cpp and HF https://huggingface.co/docs/hub/en/gguf-llamacpp
  - https://llama-cpp-python.readthedocs.io/en/latest/
- haystack llama.cpp https://haystack.deepset.ai/integrations/llama_cpp
