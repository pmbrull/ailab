"""Raw LLM endpoint"""

import os

import bentoml
import transformers
import torch
from pydantic import BaseModel, ConfigDict
from haystack_integrations.components.generators.llama_cpp import LlamaCppGenerator


MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
HF_TOKEN_KEY = "HF_TOKEN"


class LLMInput(BaseModel):
    """Input to the LLM endpoint"""

    model_config = ConfigDict(extra="forbid")

    query: str


class LLMOutput(BaseModel):
    """Output of the LLM endpoint"""

    model_config = ConfigDict(extra="forbid")

    answer: str


@bentoml.service(name="llmcpp")
class LLMCPP:
    """
    Run LLM using llama.cpp
    ```
    wget https://huggingface.co/reach-vb/llama-3-8b-Q8_0-GGUF/resolve/main/llama-3-8b.Q8_0.gguf?download=true -O llama-3-8b.Q8_0.gguf
    ```

    based on https://haystack.deepset.ai/integrations/llama_cpp
    """

    def __init__(self) -> None:
        self.generator = LlamaCppGenerator(
            model="llama-3-8b.Q8_0.gguf",
            # n_ctx=512,
            # n_batch=128,
            # model_kwargs={"n_gpu_layers": -1},
            # generation_kwargs={"max_tokens": 128, "temperature": 0.1},
        )
        self.generator.warm_up()

    @bentoml.api(route="/ask", input_spec=LLMInput)
    async def embed(self, **kwargs) -> LLMOutput:
        """Embed text.

        Pass it as **kwargs + input_spec so that the main payload becomes directly the pydantic model
        """
        input_ = LLMInput(**kwargs)
        result = self.generator.run(input_.query)
        print(result)
        return LLMOutput(answer=result["replies"][0])


@bentoml.service(name="llm")
class LLMInstruct:
    """Transformer service for embeddings"""

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=MODEL_ID,
            model_kwargs={
                "torch_dtype": torch.float16,
                # "quantization_config": {"load_in_4bit": True},
                "low_cpu_mem_usage": True,
            },
            device=self.device,
            token=os.getenv(HF_TOKEN_KEY),
        )

        self.terminators = [
            self.pipeline.tokenizer.eos_token_id,
            self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

    @bentoml.api(route="/ask", input_spec=LLMInput)
    async def embed(self, **kwargs) -> LLMOutput:
        """Embed text.

        Pass it as **kwargs + input_spec so that the main payload becomes directly the pydantic model
        """
        input_ = LLMInput(**kwargs)
        messages = [
            {"role": "user", "content": input_.query},
        ]
        prompt = self.pipeline.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        output = self.pipeline(
            prompt,
            max_new_tokens=256,
            eos_token_id=self.terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        print(output)
        return LLMOutput(answer=output)
