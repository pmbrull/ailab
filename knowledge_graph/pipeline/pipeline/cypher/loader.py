"""Ometa Cypher Converter"""

import logging
from contextlib import contextmanager
from itertools import chain
from typing import Any

from neo4j import GraphDatabase, RoutingControl

from pipeline.config import Neo4JConfig
from pipeline.cypher.node import CypherNodes
from pipeline.cypher.relationship import CypherRel


class CypherLoader:
    """Convert OM concepts into Cypher queries"""

    def __init__(self, neo4j_config: Neo4JConfig, nuke: bool = False):
        self.neo4j_config = neo4j_config
        self.db = neo4j_config.database
        self.rel_queue = []

        if nuke:
            self.nuke()

        self.node_creator = CypherNodes()
        self.rel_creator = CypherRel()

    def nuke(self) -> None:
        """Clean the database"""
        self.cypher_write_query("match (a) -[r] -> () delete a, r")
        self.cypher_write_query("match(a) delete a")

    @contextmanager
    def driver(self):
        """Define the driver for the Neo4J connection"""
        with GraphDatabase.driver(
            self.neo4j_config.uri, auth=(self.neo4j_config.user, self.neo4j_config.password)
        ) as driver:
            yield driver

    def cypher_read_query(self, query, **parameters):
        """Read data from Neo4J using Cypher queries"""
        with self.driver() as driver:
            records, _, _ = driver.execute_query(
                query,
                parameters_=parameters,
                database_=self.db,
                routing_=RoutingControl.READ,
            )
            return records

    def cypher_write_query(self, query, **parameters):
        """Write data to Neo4J using Cypher queries"""
        with self.driver() as driver:
            try:
                result = driver.execute_query(
                    query,
                    parameters_=parameters,
                    database_=self.db,
                    routing_=RoutingControl.WRITE,
                )
                return result
            except Exception as exc:
                logging.error(f"Error writing query {query} due to {exc}")

    def add_embeddings(self) -> None:
        """Return the embedding query for the entity"""
        query = """
        MATCH (n)
        CALL io.ailab.embeddings(COALESCE(n.description, n.displayName)) YIELD embedding
        CALL db.create.setNodeVectorProperty(n, 'embedding', embedding)
        """
        self.cypher_write_query(query)

    def create(self, entities: list[Any]):
        """Create the entity in Neo4J"""
        query = self.create_batch_query(entities)
        if query:
            self.cypher_write_query(query)

    def create_batch_query(self, entities: list[Any]) -> str:
        """Create a batch query for the entities"""
        return "\n".join([self.node_creator.create_query(entity) for entity in entities])

    def queue_relationships(self, entities: list[Any]) -> None:
        """Queue relationships for the entities"""
        relationships = [rel for entity in entities if (rel := self.rel_creator.create_query(entity))]
        # Flatten
        self.rel_queue.extend(list(chain(*relationships)))

    def commit_relationships(self) -> None:
        """Commit the stored relationships"""
        for query in self.rel_queue:
            self.cypher_write_query(query)
        self.rel_queue = []
