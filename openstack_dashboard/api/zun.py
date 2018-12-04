
from __future__ import absolute_import

import logging
from zunclient import api_versions
from zunclient.v1 import client as zun_client

from horizon import exceptions
from horizon.utils.memoized import memoized
from openstack_dashboard.api import base

LOG = logging.getLogger(__name__)

CONTAINER_CREATE_ATTRS = zun_client.containers.CREATION_ATTRIBUTES
CAPSULE_CREATE_ATTRS = zun_client.capsules.CREATION_ATTRIBUTES
IMAGE_PULL_ATTRS = zun_client.images.PULL_ATTRIBUTES
API_VERSION = api_versions.APIVersion(api_versions.DEFAULT_API_VERSION)


def get_auth_params_from_request(request):
    """Extracts properties needed by zunclient call from the request object.

    These will be used to memoize the calls to zunclient.
    """
    endpoint_override = ""
    try:
        endpoint_override = base.url_for(request, 'container')
    except exceptions.ServiceCatalogException:
        LOG.debug('No Container Management service is configured.')
        return None
    return (
        request.user.username,
        request.user.token.id,
        request.user.tenant_id,
        endpoint_override
    )


@memoized
def zunclient(request):
    (
        username,
        token_id,
        project_id,
        endpoint_override
    ) = get_auth_params_from_request(request)

    LOG.debug('zunclient connection created using the token "%s" and url'
              ' "%s"' % (token_id, endpoint_override))
    api_version = API_VERSION
    if API_VERSION.is_latest():
        c = zun_client.Client(
            username=username,
            project_id=project_id,
            auth_token=token_id,
            endpoint_override=endpoint_override,
            api_version=api_versions.APIVersion("1.1"),
        )
        api_version = api_versions.discover_version(c, api_version)
    c = zun_client.Client(username=username,
                          project_id=project_id,
                          auth_token=token_id,
                          endpoint_override=endpoint_override,
                          api_version=api_version)
    return c


def host_show(request, id):
    return zunclient(request).hosts.get(id)
