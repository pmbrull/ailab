"""Raw LLM endpoint"""

import os

import bentoml
import transformers
import torch
from pydantic import BaseModel, ConfigDict


MODEL_ID = "meta-llama/Meta-Llama-3-8B"
HF_TOKEN_KEY = "HF_TOKEN"


class LLMInput(BaseModel):
    """Input to the LLM endpoint"""

    model_config = ConfigDict(extra="forbid")

    query: str


class LLMOutput(BaseModel):
    """Output of the LLM endpoint"""

    model_config = ConfigDict(extra="forbid")

    answer: str


@bentoml.service(name="llm")
class LLM:
    """Transformer service for embeddings"""

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = transformers.AutoModel.from_pretrained(
            MODEL_ID, access_token=os.getenv(HF_TOKEN_KEY)
        )
        self.pipeline = transformers.pipeline(
            "llm",
            model=self.model,
            tokenizer=self.model,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map=self.device,
        )

    @bentoml.api(route="/ask", input_spec=LLMInput)
    async def embed(self, **kwargs) -> LLMOutput:
        """Embed text.

        Pass it as **kwargs + input_spec so that the main payload becomes directly the pydantic model
        """
        input_ = LLMInput(**kwargs)
        return LLMOutput(answer=self.pipeline(input_.query))
