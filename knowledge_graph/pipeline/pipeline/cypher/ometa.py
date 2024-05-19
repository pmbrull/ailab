"""Handle ometa utils"""

from metadata.generated.schema.entity.classification.classification import (
    Classification,
)
from metadata.generated.schema.entity.classification.tag import Tag
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema
from metadata.generated.schema.entity.data.glossary import Glossary
from metadata.generated.schema.entity.data.glossaryTerm import GlossaryTerm
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    AuthProvider,
    OpenMetadataConnection,
)
from metadata.generated.schema.entity.services.databaseService import DatabaseService
from metadata.generated.schema.entity.teams.team import Team
from metadata.generated.schema.entity.teams.user import User
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata

from pipeline.config import Config
from pipeline.cypher.loader import CypherLoader

ENTITIES = (
    (Team, User),
    (Classification, Tag),
    (Glossary, GlossaryTerm),
    (DatabaseService, Database, DatabaseSchema, Table),
)


class OMCypherLoader:
    """Load metadata into Neo4J"""

    def __init__(self, config: Config):
        self.config = config
        self.metadata = self.get_ometa()
        self.cypher = CypherLoader(self.config.neo4j, nuke=True)

    def get_ometa(self) -> OpenMetadata:
        """Return the OpenMetadata API"""
        server_config = OpenMetadataConnection(
            hostPort=self.config.om.uri,
            authProvider=AuthProvider.openmetadata,
            securityConfig=OpenMetadataJWTClientConfig(jwtToken=self.config.om.jwt_token),
        )
        metadata = OpenMetadata(server_config)
        assert metadata.health_check()

        return metadata

    def load(self) -> None:
        """Load metadata into Neo4j

        We group the entities in ordered tuples to ensure that the relationships are created in the correct order
        """
        for groups in ENTITIES:
            it = iter(groups)
            try:
                while True:
                    entity = next(it)
                    asset_list = self.metadata.list_all_entities(
                        entity=entity,
                        skip_on_failure=True,
                        fields=["*"],
                    )
                    list_ = list(asset_list)
                    self.cypher.create(list_)
                    self.cypher.queue_relationships(list_)
            except StopIteration:
                self.cypher.commit_relationships()
        self.cypher.add_embeddings()

    def index(self, dimensions: int, similarity_function: str) -> None:
        """Add index to the nodes"""
        self.cypher.add_index(dimensions, similarity_function)
