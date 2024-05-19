"""Converter pipeline"""

from haystack import component
from haystack.dataclasses import Document
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
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.generated.schema.type.tagLabel import TagLabel
from metadata.ingestion.ometa.ometa_api import OpenMetadata

from pipeline.config import OMConfig

ENTITIES = (
    (Team, User),
    (Classification, Tag),
    (Glossary, GlossaryTerm),
    (DatabaseService, Database, DatabaseSchema, Table),
)


CONTENT_TEMPLATE = """
type: {type}
name: {name}
description: {description}
{owner}
{tags}
domain: {domain}
"""

OWNER_TEMPLATE = """
owner:
    name: {name}
    type: {type}
"""

TAGS_TEMPLATE = """
tags:
    {tags}
glossary terms:
    {glossary_terms}
"""


@component
class CustomProducer:
    """Producer for OpenMetadata"""

    def __init__(self, config: OMConfig):
        self.config = config
        self.metadata = self.get_ometa()

    def get_ometa(self) -> OpenMetadata:
        """Return the OpenMetadata API"""
        server_config = OpenMetadataConnection(
            hostPort=self.config.uri,
            authProvider=AuthProvider.openmetadata,
            securityConfig=OpenMetadataJWTClientConfig(jwtToken=self.config.jwt_token),
        )
        metadata = OpenMetadata(server_config)
        assert metadata.health_check()

        return metadata

    def _load_documents(self) -> list[Document]:
        """Load documents from OM"""
        documents = []
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
                    for asset in asset_list:
                        documents.append(
                            Document(
                                content=self.create_content(asset),
                                id=asset.id.__root__,
                                meta={"type": entity.__name__},
                            )
                        )
            except StopIteration:
                pass

        return documents

    @component.output_types(documents=list[Document])
    def run(self):
        """Load documents from OM and return them as a list of Documents"""
        return {"documents": self._load_documents()}

    def create_content(self, entity) -> str:
        """Create the string content of an entity"""
        return CONTENT_TEMPLATE.format(
            type=entity.__class__.__name__,
            name=entity.name,
            description=entity.description,
            owner=self.create_owner_content(entity.owner) if hasattr(entity, "owner") and entity.owner else "None",
            tags=self.create_tags_content(entity.tags) if hasattr(entity, "tags") and entity.tags else "None",
            domain=entity.domain.name if hasattr(entity, "domain") and entity.domain else "None",
        )

    def create_owner_content(self, owner: EntityReference) -> str:
        """Create the string content of an owner"""
        return OWNER_TEMPLATE.format(name=owner.name, type=owner.type)

    def create_tags_content(self, tags: list[TagLabel]) -> str:
        """Create the string content of an owner"""
        return TAGS_TEMPLATE.format(
            tags=", ".join([tag.tagFQN.__root__ for tag in tags if tag.source.value == "Classification"]),
            glossary_terms=", ".join([tag.tagFQN.__root__ for tag in tags if tag.source.value == "Glossary"]),
        )
