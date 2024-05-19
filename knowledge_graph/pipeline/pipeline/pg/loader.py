"""PG Loader"""

# https://docs.haystack.deepset.ai/docs/outputadapter follow the custom DocumentProducer
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.writers import DocumentWriter
from haystack.core.pipeline.pipeline import Pipeline
from haystack.utils import Secret
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

from pipeline.config import Config
from pipeline.pg.embedder import CustomEmbedder
from pipeline.pg.producer import CustomProducer

SEARCH_STRATEGY = "hnsw"
VECTOR_FUNCTION = "cosine_similarity"
TABLE_NAME = "embeddings"


TEMPLATE = """
You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question.
Do not mention that you based the results on the given information.
If the provided information is empty, say that you don't know the answer.

Information:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{ query }}?
"""


class PGLoader:
    """Load data into Postgres"""

    def __init__(self, config: Config, nuke: bool = True):
        self.config = config
        self.nuke = nuke

        self.document_store = PgvectorDocumentStore(
            connection_string=Secret.from_token(config.pg.uri()),
            table_name=TABLE_NAME,
            embedding_dimension=384,
            vector_function=VECTOR_FUNCTION,
            recreate_table=self.nuke,
            hnsw_recreate_index_if_exists=self.nuke,
            search_strategy=SEARCH_STRATEGY,
        )

        self.index = Pipeline()
        self.index.add_component("converter", CustomProducer(self.config.om))
        self.index.add_component("writer", DocumentWriter(self.document_store))
        self.index.add_component("embedder", CustomEmbedder(config.llm.embedding_model_uri))
        self.index.connect("converter", "embedder")
        self.index.connect("embedder", "writer")

        self.query = Pipeline()
        self.query.add_component("embedder", CustomEmbedder(config.llm.embedding_model_uri))
        self.query.add_component("retriever", PgvectorEmbeddingRetriever(self.document_store, top_k=5))
        self.query.add_component("prompt_builder", PromptBuilder(template=TEMPLATE))

    def load(self):
        """Run the pipeline"""
        self.index.run(data={})

    def ask(self, query: str):
        """Ask the document store"""
        return self.document_store.query_by_embedding(query)
