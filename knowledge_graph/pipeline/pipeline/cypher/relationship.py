"""Create Cypher relationships for the entities"""

from functools import singledispatchmethod

from metadata.generated.schema.entity.teams.team import Team
from metadata.generated.schema.entity.teams.user import User

from pipeline.cypher.base import CypherBase


class CypherRel(CypherBase):
    """Create relationship queries"""

    @singledispatchmethod
    def create_query(self, entity) -> list[str]:
        """Create a Cypher query for the entity"""
        raise NotImplementedError(f"Entity {type(entity).__name__} not supported")

    @create_query.register
    def _(self, entity: Team) -> list[str]:
        """Create team relationship"""
        rel_ = []
        if entity.children and entity.children.__root__:
            children_match = ",\n".join(
                [
                    f"({self._get_unique_id(child)}:Team {{fullyQualifiedName: '{child.fullyQualifiedName}'}})"
                    for child in entity.children.__root__
                ]
            )
            children_rel = "\n".join(
                [f"CREATE (t)-[:HAS]->({self._get_unique_id(child)})" for child in entity.children.__root__]
            )
            rel_.append(f"""
            MATCH 
              (t:Team {{fullyQualifiedName: '{entity.fullyQualifiedName.__root__}'}}),
              {children_match} 
            {children_rel} 
            """)

        if entity.users and entity.users.__root__:
            users_match = ",\n".join(
                [
                    f"({self._get_unique_id(user)}:User {{fullyQualifiedName: '{user.fullyQualifiedName}'}})"
                    for user in entity.users.__root__
                ]
            )
            users_rel = "\n".join(
                [f"CREATE (t)-[:CONTAINS]->({self._get_unique_id(user)})" for user in entity.users.__root__]
            )
            rel_.append(f"""
            MATCH 
              (t:Team {{fullyQualifiedName: '{entity.fullyQualifiedName.__root__}'}}),
              {users_match} 
            {users_rel} 
            """)

        return rel_

    @create_query.register
    def _(self, entity: User) -> list[str]:
        """Nothing to do for Users"""
