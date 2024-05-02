"""Populate Neo4J with the data from the glossary"""


def load() -> None:
    """Load metadata into Neo4j"""
    # metadata: OpenMetadata = get_ometa(CONFIG.om)


def run() -> None:
    """Run the workflow"""
    load()


if __name__ == "__main__":
    """source .env first"""
    run()
