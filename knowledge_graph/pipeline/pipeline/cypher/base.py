"""Cyper Base class"""

import abc


class CypherBase(abc.ABC):
    """Base methods"""

    @staticmethod
    def _get_unique_id(entity) -> str:
        return f"`{str(entity.id.__root__)}`"

    @abc.abstractmethod
    def create_query(self, entity) -> str | list[str]:
        """Create a Cypher query for the entity"""
        raise NotImplementedError(f"Entity {type(entity).__name__} not supported")
