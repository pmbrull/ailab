"""Populate Neo4J with the data from the glossary"""

from pipeline.config import CONFIG
from pipeline.ometa import OMCypherLoader


def run() -> None:
    """Run the workflow"""
    loader = OMCypherLoader(CONFIG)
    loader.load()


if __name__ == "__main__":
    """source .env first"""
    run()
