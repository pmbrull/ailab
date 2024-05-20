"""Populate Neo4J with the data from the glossary"""

import logging

from pipeline.config import CONFIG
from pipeline.pg.ask import PGAsker
from pipeline.pg.loader import PGLoader

METADATA_LOGGER = "ailab"
BASE_LOGGING_FORMAT = "[%(asctime)s] %(levelname)-8s {%(name)s:%(module)s:%(lineno)d} - %(message)s"
logging.basicConfig(format=BASE_LOGGING_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")


def run() -> None:
    """Run the workflow"""
    # loader = OMCypherLoader(CONFIG)
    reload = True
    if reload:
        loader = PGLoader(CONFIG, nuke=True)
        loader.load()

    asker = PGAsker(CONFIG)

    # question = "How many tables do we have?"
    # The answer to this is based on the top_k retrieved documents. We'll need to add a summary context document.
    question = "What is the description of the Table dim_customer?"
    answer = asker.ask(question)
    logging.info(answer)
    # print(answer)


if __name__ == "__main__":
    """source .env first"""
    run()
