"""Handle ometa utils"""

from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    AuthProvider,
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata

from pipeline.config import OMSettings


def get_ometa(settings: OMSettings) -> OpenMetadata:
    """Return the OpenMetadata API"""
    server_config = OpenMetadataConnection(
        hostPort=settings.uri,
        authProvider=AuthProvider.openmetadata,
        securityConfig=OpenMetadataJWTClientConfig(jwtToken=settings.jwt_token),
    )
    metadata = OpenMetadata(server_config)
    assert metadata.health_check()

    return metadata
