"""PG Asker"""

# https://docs.haystack.deepset.ai/docs/outputadapter follow the custom DocumentProducer
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.core.pipeline.pipeline import Pipeline
from haystack.utils import Secret
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

from pipeline.config import Config
from pipeline.pg.embedder import CustomEmbedder

"""
The documents describe assets in a Data Platform and have the following structure:
- type: Type of the asset. 
- name: Name of the asset. 
- description: Description of the asset.
- owner: Team or user that owns the asset.
- domain: Domain of the asset.
"""


TEMPLATE = """
You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
You must only answer the question based on the information given below.
Make the answer sound as a response to the question.
Do not mention that you based the results on the given information.
If the provided information is empty, say that you don't know the answer.

Use the description of the assets, its type and any other relevant information about their children to
answer the questions. No other information should be used.

If you are asked about an asset, in the response provide a link to the asset. The link can be found in he asset href field.
When answering, give information about the asset owner, domain and tags, if they exist.

Information:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{ query }}?
"""


class PGAsker:
    """Load data into Postgres"""

    def __init__(self, config: Config):
        self.config = config

        self.document_store = PgvectorDocumentStore(
            connection_string=Secret.from_token(config.pg.uri()),
            table_name=config.llm.table_name,
            embedding_dimension=config.llm.embedding_model_dim,
            vector_function=config.llm.vector_function,
            recreate_table=False,
            hnsw_recreate_index_if_exists=False,
            search_strategy=config.llm.search_strategy,
        )

        self.query = Pipeline()
        self.query.add_component("embedder", CustomEmbedder(config.llm.embedding_model_uri))
        self.query.add_component("retriever", PgvectorEmbeddingRetriever(document_store=self.document_store))
        self.query.add_component("prompt_builder", PromptBuilder(template=TEMPLATE))
        self.query.add_component(
            "llm",
            OllamaGenerator(model="llama3", url="http://localhost:11434/api/generate"),
        )
        self.query.add_component("answer_builder", AnswerBuilder())
        self.query.connect("embedder.embedding", "retriever.query_embedding")
        self.query.connect("retriever", "prompt_builder.documents")
        self.query.connect("prompt_builder", "llm")
        self.query.connect("llm.replies", "answer_builder.replies")
        self.query.connect("llm.meta", "answer_builder.meta")
        self.query.connect("retriever", "answer_builder.documents")

    def ask(self, question: str):
        """Ask the document store"""
        return self.query.run(
            {
                "embedder": {"text": question},
                "retriever": {"top_k": 3},
                "prompt_builder": {"query": question},
                "answer_builder": {"query": question},
            }
        )
