"""Create Cypher relationships for the entities"""

from functools import singledispatchmethod

from metadata.generated.schema.entity.classification.classification import (
    Classification,
)
from metadata.generated.schema.entity.classification.tag import Tag
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema
from metadata.generated.schema.entity.data.glossary import Glossary
from metadata.generated.schema.entity.data.glossaryTerm import GlossaryTerm
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.services.databaseService import DatabaseService
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
                [f"CREATE (t)-[:CONTAINS]->({self._get_unique_id(child)})" for child in entity.children.__root__]
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

    @create_query.register(User)
    @create_query.register(Classification)
    @create_query.register(Glossary)
    def _(self, entity) -> list[str]:
        """Nothing to do"""

    @create_query.register
    def _(self, entity: Tag) -> list[str]:
        """Create relationship with the classification"""
        rel_ = []
        if entity.classification:
            rel_.append(f"""
            MATCH 
              (t:Tag {{fullyQualifiedName: '{entity.fullyQualifiedName}'}}),
              (c:Classification {{fullyQualifiedName: '{entity.classification.fullyQualifiedName}'}}) 
            CREATE (c)-[:CONTAINS]->(t) 
            """)

        return rel_

    @create_query.register
    def _(self, entity: GlossaryTerm) -> list[str]:
        """Create relationship with the classification"""
        rel_ = []
        if entity.parent:
            rel_.append(f"""
                MATCH 
                  (t:GlossaryTerm {{fullyQualifiedName: '{entity.fullyQualifiedName.__root__}'}}),
                  (p:GlossaryTerm {{fullyQualifiedName: '{entity.parent.fullyQualifiedName}'}})
                CREATE (p)-[:CONTAINS]->(t) 
                """)

        if entity.glossary:
            rel_.append(f"""
                MATCH 
                  (t:GlossaryTerm {{fullyQualifiedName: '{entity.fullyQualifiedName.__root__}'}}),
                  (p:Glossary {{fullyQualifiedName: '{entity.glossary.fullyQualifiedName}'}})
                CREATE (p)-[:CONTAINS]->(t) 
                """)

        if entity.relatedTerms and entity.relatedTerms.__root__:
            terms_match = ",\n".join(
                [
                    f"({self._get_unique_id(term)}:GlossaryTerm {{fullyQualifiedName: '{term.fullyQualifiedName}'}})"
                    for term in entity.relatedTerms.__root__
                ]
            )
            terms_rel = "\n".join(
                [f"CREATE (t)-[:RELATED_TO]->({self._get_unique_id(term)})" for term in entity.relatedTerms.__root__]
            )
            rel_.append(f"""
                MATCH 
                  (t:GlossaryTerm {{fullyQualifiedName: '{entity.fullyQualifiedName.__root__}'}}),
                  {terms_match} 
                {terms_rel} 
                """)

        return rel_

    @create_query.register(DatabaseService)
    @create_query.register(Database)
    @create_query.register(DatabaseSchema)
    @create_query.register(Table)
    def _(self, entity) -> list[str]:
        """Nothing to do"""
