"""Memgraph client for interacting with Memgraph database."""

from typing import Any

import neo4j
from langchain.graphs import Neo4jGraph
from neo4j.exceptions import CypherSyntaxError

SCHEMA_QUERY = """
CALL llm_util.schema()
YIELD *
RETURN *
"""


class MemgraphGraph(Neo4jGraph):
    """Memgraph wrapper for graph ops"""

    def __init__(self, url: str, username: str, password: str, database: str = "memgraph") -> None:
        """Create a new Memgraph wrapper"""
        super().__init__(url, username, password, database)
        self._driver = neo4j.GraphDatabase.driver(url, auth=(username, password))
        self._database = database
        self.schema = None

        try:
            self._driver.verify_connectivity()
        except neo4j.exceptions.ServiceUnavailable as err:
            raise ValueError(f"Unable to connect to Memgraph due to {err}")

    def query(self, query: str, params: dict | None = None) -> list[dict[str, Any]]:
        """Execute a query"""
        # print(query, params)
        with self._driver.session(database=self._database) as session:
            try:
                data = session.run(query, params)
                # Hard list of 50 results
                return [record.data() for record in data][:50]
            except CypherSyntaxError as err:
                raise ValueError(f"Generated Cypher Statement is not valid: {err}")

    def refresh_schema(self) -> None:
        """Refresh the schema"""
        self.schema = self.query(SCHEMA_QUERY)[0].get("schema")
        # print(self.schema)
