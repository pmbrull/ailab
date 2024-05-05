"""Ometa Cypher Converter"""

from contextlib import contextmanager
from functools import singledispatchmethod
from typing import Any

from metadata.generated.schema.entity.teams.team import Team
from metadata.generated.schema.entity.teams.user import User
from neo4j import GraphDatabase, RoutingControl

from pipeline.config import Neo4JConfig


class CypherLoader:
    """Convert OM concepts into Cypher queries"""

    def __init__(self, neo4j_config: Neo4JConfig, nuke: bool = False):
        self.neo4j_config = neo4j_config
        self.db = neo4j_config.database

        if nuke:
            self.nuke()

    def nuke(self) -> None:
        """Clean the database"""
        self.cypher_write_query("match(a) delete a")
        self.cypher_write_query("match (a) -[r] -> () delete a, r")

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
            result = driver.execute_query(
                query,
                parameters_=parameters,
                database_=self.db,
                routing_=RoutingControl.WRITE,
            )
            return result

    def add_embeddings(self) -> None:
        """Return the embedding query for the entity"""
        query = """
        MATCH (n)
        WHERE n.description IS NOT NULL
        CALL io.ailab.embeddings(n.description) YIELD embedding
        CALL db.create.setNodeVectorProperty(n, 'embedding', embedding)
        """
        self.cypher_write_query(query)

    @staticmethod
    def _add_description(entity) -> str:
        """Add description clause if needed"""
        return f", description: '{entity.description.__root__}'" if entity.description else ""

    @staticmethod
    def _get_unique_id(entity) -> str:
        return f"`{str(entity.id.__root__)}`"

    def create(self, entities: list[Any]):
        """Create the entity in Neo4J"""
        query = self.create_batch_query(entities)
        self.cypher_write_query(query)

    def create_batch_query(self, entities: list[Any]) -> str:
        """Create a batch query for the entities"""
        return "\n".join([self.create_query(entity) for entity in entities])

    @singledispatchmethod
    def create_query(self, entity) -> str:
        """Create a Cypher query for the entity"""
        raise NotImplementedError(f"Entity {type(entity).__name__} not supported")

    @create_query.register
    def _(self, entity: Team) -> str:
        """Create team"""
        return f"""
        CREATE ({self._get_unique_id(entity)}:Team {{
            name: '{entity.name.__root__}',
            fullyQualifiedName: '{entity.fullyQualifiedName.__root__}',
            displayName: '{entity.displayName or entity.name.__root__}',
            type: '{entity.teamType.value}'
            {self._add_description(entity)}
        }})
        """

    @create_query.register
    def _(self, entity: User) -> str:
        """Create user"""
        return f"""
            CREATE ({self._get_unique_id(entity)}:User {{
                name: '{entity.name.__root__}',
                fullyQualifiedName: '{entity.fullyQualifiedName.__root__}',
                displayName: '{entity.displayName or entity.name.__root__}',
                email: '{entity.email.__root__}'
                {self._add_description(entity)}
            }})
            """
