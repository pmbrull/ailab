"""Create Cypher nodes for the entities"""

from functools import singledispatchmethod

from metadata.generated.schema.entity.classification.classification import (
    Classification,
)
from metadata.generated.schema.entity.classification.tag import Tag
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

    @create_query.register
    def _(self, entity: Classification) -> str:
        """Create user"""
        return f"""
            CREATE ({self._get_unique_id(entity)}:Classification {{
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

    @create_query.register
    def _(self, entity: Tag) -> str:
        """Create user"""
        return f"""
            CREATE ({self._get_unique_id(entity)}:Tag {{
                name: '{entity.name.__root__}',
                fullyQualifiedName: '{entity.fullyQualifiedName}',
                displayName: '{entity.displayName or entity.name.__root__}',
                mutuallyExclusive: '{entity.mutuallyExclusive}',
                provider: '{entity.provider.value}',
                disabled: {str(entity.disabled).lower() if entity.disabled is not None else 'false'},
                usageCount: {entity.usageCount}
                {self._add_description(entity)}
            }})
            """
