"""PG Loader"""

from haystack.components.writers import DocumentWriter
from haystack.core.pipeline.pipeline import Pipeline
from haystack.document_stores.types import DuplicatePolicy
from haystack.utils import Secret
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

from pipeline.config import Config
from pipeline.pg.embedder import CustomDocumentEmbedder
from pipeline.pg.producer import CustomProducer

SEARCH_STRATEGY = "hnsw"
VECTOR_FUNCTION = "cosine_similarity"
TABLE_NAME = "embeddings"


class PGLoader:
    """Load data into Postgres"""

    def __init__(self, config: Config, nuke: bool = False):
        self.config = config
        self.nuke = nuke

        self.document_store = PgvectorDocumentStore(
            connection_string=Secret.from_token(config.pg.uri()),
            table_name=TABLE_NAME,
            embedding_dimension=1024,
            vector_function=VECTOR_FUNCTION,
            recreate_table=self.nuke,
            hnsw_recreate_index_if_exists=self.nuke,
            search_strategy=SEARCH_STRATEGY,
        )

        self.index = Pipeline()
        self.index.add_component("converter", CustomProducer(self.config.om))
        self.index.add_component("writer", DocumentWriter(self.document_store, policy=DuplicatePolicy.SKIP))
        self.index.add_component("embedder", CustomDocumentEmbedder(config.llm.embedding_model_uri))
        self.index.connect("converter", "embedder")
        self.index.connect("embedder", "writer")

    def load(self):
        """Run the pipeline"""
        self.index.run(data={})
