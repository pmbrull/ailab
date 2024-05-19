"""Custom haystack embedder component"""

import httpx
from haystack import component
from haystack.dataclasses import Document


@component
class CustomEmbedder:
    """Call our custom embedding API"""

    def __init__(self, uri: str) -> None:
        self.uri = uri

    @component.output_types(documents=list[Document])
    def run(self, documents: list[Document]):
        """Add embeddings to the documents"""
        for doc in documents:
            text = doc.content
            query_embedding = httpx.post(self.uri, data={"text": text})
            doc.embedding = query_embedding.json().get("embedding")

        return {"documents": documents}
