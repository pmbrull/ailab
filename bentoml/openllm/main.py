import os
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from metadata.generated.schema.entity.data.glossary import Glossary
from metadata.generated.schema.entity.data.glossaryTerm import GlossaryTerm

### Prep Dataset
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata

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
dataset = [
    f"{term.displayName or term.name} is {term.description.__root__}"
    for term in terms.entities
]

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
qdrant_vec_store = Qdrant.from_texts(
    dataset, embedding_model, host="localhost", port=6333
)

llm = Ollama(model="llama2")
rag = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=qdrant_vec_store.as_retriever(),
    return_source_documents=False,
)

res = rag.invoke("What do the branch assets include in the glossary?")
print(res)
