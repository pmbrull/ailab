"""Converter pipeline"""

from functools import singledispatchmethod

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
from metadata.generated.schema.entity.data.table import Column, Table
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
The {type} called "{name}" contains the following information: "{description}"
{children}

It is owner by {owner}.
It is tagged with: {tags}.
It belongs to the {domain} domain.
"""

OWNER_TEMPLATE = """
the {type} "{name}"
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
                        content = self.create_content(asset)
                        documents.append(
                            Document(
                                content=content,
                                id=asset.id.__root__,
                                meta={"type": entity.__name__},
                            )
                        )
            except StopIteration:
                pass

        return documents

    def _get_fqn(self, entity) -> str:
        return f"`{self._clean_str(entity.fullyQualifiedName.__root__)}`"

    @staticmethod
    def _clean_str(value: str) -> str:
        """Clean the string for Cypher"""
        return value.replace("'", "\\'").replace('"', '\\"')

    @component.output_types(documents=list[Document])
    def run(self):
        """Load documents from OM and return them as a list of Documents"""
        return {"documents": self._load_documents()}

    @singledispatchmethod
    def create_content(self, entity) -> str:
        """Create the string content of an entity"""
        return CONTENT_TEMPLATE.format(
            type=entity.__class__.__name__,
            name=entity.displayName or entity.name.__root__,
            description=entity.description.__root__ if entity.description else "None",
            owner=self.create_owner_content(entity.owner)
            if hasattr(entity, "owner") and entity.owner
            else "owner: None",
            tags=self.create_tags_content(entity.tags) if hasattr(entity, "tags") and entity.tags else "tags: None",
            domain=entity.domain.name if hasattr(entity, "domain") and entity.domain else "None",
            children=None,
        )

    def _add_cols_rec(self, col: Column, parent_label: str, create: list[str], table: Table):
        """Add col and its parent"""
        create.append(f"""
            - column: 
                - name: {col.displayName or col.name.__root__}
                - parent: {parent_label}
                - href: {table.href.__root__}
                - data type: {col.dataTypeDisplay}
                - description: {col.description.__root__ if col.description else "None"}
        """)
        for child in col.children or []:
            self._add_cols_rec(col=child, parent_label=self._get_fqn(col), create=create, table=table)

    @create_content.register
    def _(self, entity: Table) -> str:
        """Create the string content of a Table"""
        columns = []
        for col in entity.columns:
            self._add_cols_rec(col, entity.fullyQualifiedName.__root__, columns, entity)
        return CONTENT_TEMPLATE.format(
            type=entity.__class__.__name__,
            name=entity.name.__root__,
            description=entity.description.__root__ if entity.description else "None",
            owner=self.create_owner_content(entity.owner)
            if hasattr(entity, "owner") and entity.owner
            else "owner: None",
            tags=self.create_tags_content(entity.tags) if hasattr(entity, "tags") and entity.tags else "tags: None",
            domain=entity.domain.name if hasattr(entity, "domain") and entity.domain else "None",
            children="\n".join(columns),
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
