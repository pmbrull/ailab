"""Pipeline settings"""

import logging
from os.path import expandvars
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

CONFIG_PATH = Path(__file__).parent.parent / "conf" / "pipeline.yaml"


class Neo4JSettings(BaseModel):
    """Neo4J settings"""

    uri: str = Field(..., description="URI of the Neo4J database connection")
    user: str = Field(..., description="User for the Neo4J database connection")
    password: str = Field(..., description="Password for the Neo4J connection")
    database: str = Field(..., description="Database for the Neo4J connection")


class OMSettings(BaseModel):
    """OpenMetadata settings"""

    uri: str = Field(..., description="Host and port of the OpenMetadata API")
    jwt_token: str = Field(..., description="JWT token for the OpenMetadata API")


class Config(BaseModel):
    """Pipeline settings"""

    neo4j: Neo4JSettings
    om: OMSettings


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
