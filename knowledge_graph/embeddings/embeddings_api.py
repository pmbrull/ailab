"""Embeddings API"""

import bentoml
import torch
from numpy import ndarray
from pydantic import BaseModel, ConfigDict, Field
from sentence_transformers import SentenceTransformer


class TransformerInput(BaseModel):
    """Simple text input"""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="Text to embed")


class TransformerOutput(BaseModel):
    """Simple text input"""

    model_config = ConfigDict(extra="forbid")

    embedding: ndarray = Field(..., description="embedded text")


@bentoml.service(name="transformer")
class Transformer:
    """Transformer service for embeddings"""

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=self.device)

    @bentoml.api(route="/embed", input_spec=TransformerInput)
    async def embed(self, **kwargs) -> TransformerOutput:
        """Embed text.

        Pass it as **kwargs + input_spec so that the main payload becomes directly the pydantic model
        """
        input_ = TransformerInput(**kwargs)
        return TransformerOutput(embedding=self.model.encode(input_.text))
