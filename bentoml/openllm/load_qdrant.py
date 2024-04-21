"""
Load data into Qdrant index
ref: https://www.gptechblog.com/from-huggingface-dataset-to-qdrant-vector-database-in-12-minutes-flat/
"""

import os
import torch
from qdrant_client import models, QdrantClient
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer

from metadata.generated.schema.entity.data.glossary import Glossary
from metadata.generated.schema.entity.data.glossaryTerm import (
    GlossaryTerm,
)
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata

# Determine device based on GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")


server_config = OpenMetadataConnection(
    hostPort="https://sandbox.open-metadata.org/api",
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(jwtToken=os.getenv("SBX_JWT")),
)
metadata = OpenMetadata(server_config)

assert metadata.health_check()

# https://sandbox.open-metadata.org/glossary/ETL
glossary = metadata.get_by_name(entity=Glossary, fqn="ETL")
terms = metadata.list_entities(
    entity=GlossaryTerm,
    params={"glossary": str(glossary.id.__root__), "limit": 10000},
    fields=["children", "owner", "parent"],
    skip_on_failure=True,
)
print(len(terms.entities))

# Load the desired model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=device)

dataset = [
    f"{term.displayName or term.name} is {term.description.__root__}"
    for term in terms.entities
]
embeddings = [model.encode(sentence) for sentence in dataset]

client = QdrantClient("localhost", port=6333)
try:
    client.create_collection(
        collection_name="glossary",
        vectors_config=models.VectorParams(
            size=model.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE,
        ),
    )
except Exception:
    # maybe already exists
    pass

points = []
# PointStruct(id=1, vector=list(embeddings[1]), payload={"term": dataset[1]})
for i in range(len(dataset)):
    # Convert numpy to float
    vector_ = [float(x) for x in embeddings[i]]
    points.append(PointStruct(id=i, vector=vector_, payload={"term": dataset[i]}))

client.upsert(collection_name="glossary", points=points, wait=True)
