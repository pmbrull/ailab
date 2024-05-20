"""Pipeline settings"""

import logging
from os.path import expandvars
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

CONFIG_PATH = Path(__file__).parent.parent / "conf" / "pipeline.yaml"


class Neo4JConfig(BaseModel):
    """Neo4J settings"""

    uri: str = Field(..., description="URI of the Neo4J database connection")
    user: str = Field(..., description="User for the Neo4J database connection")
    password: str = Field(..., description="Password for the Neo4J connection")
    database: str = Field(..., description="Database for the Neo4J connection")


class PGConfig(BaseModel):
    """Postgres settings"""

    host: str = Field(..., description="Host and port of the Postgres database connection")
    user: str = Field(..., description="User for the Postgres database connection")
    password: str = Field(..., description="Password for the Postgres connection")
    database: str = Field(..., description="Database for the Postgres connection")

    def uri(self) -> str:
        """Prep the URI"""
        return f"postgresql://{self.user}:{self.password}@{self.host}/{self.database}"


class OMConfig(BaseModel):
    """OpenMetadata settings"""

    uri: str = Field(..., description="Host and port of the OpenMetadata API")
    jwt_token: str = Field(..., description="JWT token for the OpenMetadata API")


class LLMConfig(BaseModel):
    """LLM settings"""

    embedding_model_uri: str = Field(..., description="URI of the LLM model")
    embedding_model_dim: int = Field(..., description="Dimension of the embedding model")
    search_strategy: str = Field("hnsw", description="Search strategy for the embeddings")
    vector_function: str = Field("cosine_similarity", description="Vector function for the embeddings")
    table_name: str = Field("embeddings", description="Table name for the embeddings")


class Config(BaseModel):
    """Pipeline settings"""

    neo4j: Neo4JConfig
    pg: PGConfig
    om: OMConfig
    llm: LLMConfig


def load_config(path: Path) -> Config:
    """Load the manifest from the path"""
    try:
        with path.open() as config_file:
            raw_config = config_file.read()
            expanded = expandvars(raw_config)
        config = yaml.safe_load(expanded)
        return Config(**config)
    except yaml.error.YAMLError as exc:
        logging.error(f"Cannot load manifest in [{path}] due to [{exc}]")
        raise exc


CONFIG = load_config(CONFIG_PATH)
