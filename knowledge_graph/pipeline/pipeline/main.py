"""Populate Neo4J with the data from the glossary"""

import logging

from pipeline.config import CONFIG
from pipeline.ometa import OMCypherLoader

METADATA_LOGGER = "ailab"
BASE_LOGGING_FORMAT = "[%(asctime)s] %(levelname)-8s {%(name)s:%(module)s:%(lineno)d} - %(message)s"
logging.basicConfig(format=BASE_LOGGING_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")


def run() -> None:
    """Run the workflow"""
    loader = OMCypherLoader(CONFIG)
    loader.load()
    # TODO: How to index all nodes?
    # loader.index(
    #     dimensions=384,
    #     similarity_function="cosine",
    # )


if __name__ == "__main__":
    """source .env first"""
    run()
