"""Cyper Base class"""

import abc


class CypherBase(abc.ABC):
    """Base methods"""

    @staticmethod
    def _get_unique_id(entity) -> str:
        return f"`{str(entity.id.__root__)}`"

    def _get_fqn(self, entity) -> str:
        return f"`{self._clean_str(entity.fullyQualifiedName.__root__)}`"

    @staticmethod
    def _clean_str(value: str) -> str:
        """Clean the string for Cypher"""
        return value.replace("'", "\\'").replace('"', '\\"')

    @abc.abstractmethod
    def create_query(self, entity) -> str | list[str]:
        """Create a Cypher query for the entity"""
        raise NotImplementedError(f"Entity {type(entity).__name__} not supported")
