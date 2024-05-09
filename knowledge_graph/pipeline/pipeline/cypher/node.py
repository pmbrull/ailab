"""Create Cypher nodes for the entities"""

from functools import singledispatchmethod

from metadata.generated.schema.entity.classification.classification import (
    Classification,
)
from metadata.generated.schema.entity.classification.tag import Tag
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema
from metadata.generated.schema.entity.data.glossary import Glossary
from metadata.generated.schema.entity.data.glossaryTerm import GlossaryTerm
from metadata.generated.schema.entity.data.table import Column, Table
from metadata.generated.schema.entity.services.databaseService import DatabaseService
from metadata.generated.schema.entity.teams.team import Team
from metadata.generated.schema.entity.teams.user import User

from pipeline.cypher.base import CypherBase


class CypherNodes(CypherBase):
    """Create node queries"""

    def _add_description(self, entity) -> str:
        """Add description clause if needed"""
        return f", description: '{self._clean_str(entity.description.__root__)}'" if entity.description else ""

    @singledispatchmethod
    def create_query(self, entity) -> str:
        """Create a Cypher query for the entity"""
        raise NotImplementedError(f"Entity {type(entity).__name__} not supported")

    @create_query.register
    def _(self, entity: Team) -> str:
        """Create team"""
        return f"""
            CREATE ({self._get_unique_id(entity)}:{type(entity).__name__} {{
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
            CREATE ({self._get_unique_id(entity)}:{type(entity).__name__} {{
                name: '{entity.name.__root__}',
                fullyQualifiedName: '{entity.fullyQualifiedName.__root__}',
                displayName: '{entity.displayName or entity.name.__root__}',
                email: '{entity.email.__root__}'
                {self._add_description(entity)}
            }})
            """

    @create_query.register(Classification)
    @create_query.register(Glossary)
    def _(self, entity) -> str:
        """Create user"""
        return f"""
            CREATE ({self._get_unique_id(entity)}:{type(entity).__name__} {{
                name: '{entity.name.__root__}',
                fullyQualifiedName: '{entity.fullyQualifiedName.__root__}',
                displayName: '{entity.displayName or entity.name.__root__}',
                mutuallyExclusive: '{entity.mutuallyExclusive}',
                provider: '{entity.provider.value}',
                disabled: {str(entity.disabled).lower() if entity.disabled is not None else 'false'},
                termCount: '{entity.termCount}'
                {self._add_description(entity)}
            }})
            """

    @create_query.register(Tag)
    @create_query.register(GlossaryTerm)
    def _(self, entity) -> str:
        """Create user"""
        fqn = (
            entity.fullyQualifiedName.__root__
            if hasattr(entity.fullyQualifiedName, "__root__")
            else entity.fullyQualifiedName
        )
        return f"""
            CREATE ({self._get_unique_id(entity)}:{type(entity).__name__} {{
                name: '{entity.name.__root__}',
                fullyQualifiedName: '{fqn}',
                displayName: '{entity.displayName or entity.name.__root__}',
                mutuallyExclusive: '{entity.mutuallyExclusive}',
                provider: '{entity.provider.value}',
                disabled: {str(entity.disabled).lower() if entity.disabled is not None else 'false'},
                usageCount: {entity.usageCount}
                {self._add_description(entity)}
            }})
            """

    @create_query.register(DatabaseService)
    @create_query.register(Database)
    @create_query.register(DatabaseSchema)
    def _(self, entity) -> str:
        """Create database service"""
        return f"""
            CREATE ({self._get_unique_id(entity)}:{type(entity).__name__} {{
                name: '{entity.name.__root__}',
                fullyQualifiedName: '{entity.fullyQualifiedName.__root__}',
                displayName: '{entity.displayName or entity.name.__root__}',
                serviceType: '{entity.serviceType.value}'
                {self._add_description(entity)}
            }})
            """

    def _add_cols_rec(self, col: Column, parent_label: str, create: list[str]):
        """Add col and its parent"""
        create.append(f"""
            CREATE ({self._get_fqn(col)}:Column {{
                name: '{col.name.__root__}',
                fullyQualifiedName: '{col.fullyQualifiedName.__root__}',
                displayName: '{col.displayName or col.name.__root__}',
                dataType: '{col.dataType.value}',
                dataTypeDisplay: '{col.dataTypeDisplay}',
                jsonSchema: '{col.jsonSchema}'
                {self._add_description(col)}
            }})
            CREATE ({parent_label})-[:CONTAINS]->({self._get_fqn(col)})
        """)
        for child in col.children or []:
            self._add_cols_rec(col=child, parent_label=self._get_fqn(col), create=create)

    @create_query.register
    def _(self, entity: Table) -> str:
        """Create table. Here we make an exception and already add the relationships to the columns for simplicity"""
        create = [
            f"""
            CREATE ({self._get_unique_id(entity)}:{type(entity).__name__} {{
                name: '{entity.name.__root__}',
                fullyQualifiedName: '{entity.fullyQualifiedName.__root__}',
                displayName: '{entity.displayName or entity.name.__root__}',
                tableType: '{entity.tableType.value if entity.tableType else None}',
                serviceType: '{entity.serviceType.value}',
                retentionPeriod: '{entity.retentionPeriod.__root__ if entity.retentionPeriod else None}',
                schemaDefinition: '{self._clean_str(entity.schemaDefinition.__root__) if entity.schemaDefinition else None}'
                {self._add_description(entity)}
            }})
            """
        ]
        for col in entity.columns:
            self._add_cols_rec(col=col, parent_label=self._get_unique_id(entity), create=create)

        return "\n".join(create)
