"""Embeddings API"""

import bentoml
import torch
from pydantic import BaseModel, ConfigDict, Field
from sentence_transformers import SentenceTransformer


class TransformerInput(BaseModel):
    """Simple text input"""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="Text to embed")


class TransformerOutput(BaseModel):
    """Simple text input"""

    model_config = ConfigDict(extra="forbid")

    embedding: list[float] = Field(..., description="embedded text")


@bentoml.service(name="transformer")
class Transformer:
    """Transformer service for embeddings"""

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        dimensions = 1024
        self.model = SentenceTransformer(
            "mixedbread-ai/mxbai-embed-large-v1", device=self.device, truncate_dim=dimensions
        )
        # ollama.pull("mxbai-embed-large")

    @bentoml.api(route="/embed", input_spec=TransformerInput)
    async def embed(self, **kwargs) -> TransformerOutput:
        """Embed text.

        Pass it as **kwargs + input_spec so that the main payload becomes directly the pydantic model
        """
        query = "Represent this sentence for searching relevant passages: {text}"
        input_ = TransformerInput(**kwargs)
        # res = ollama.embeddings(
        #    model="mxbai-embed-large",
        #    prompt=input_.text,
        # )
        return TransformerOutput(embedding=self.model.encode(query.format(text=input_.text)))
