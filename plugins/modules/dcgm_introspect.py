# -*- coding: utf-8 -*-
# Copyright (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for retrieve dcgm introspection data."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dcgm_introspect
short_description: Retrieve DCGM introspection data
description:
    - Retrieve DCGM introspection data using the NVIDIA REST API.
    - This module requires the C(requests) Python library.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description:
            - The desired state of the resource.
        type: str
        choices:
            - present
            - absent
        default: present
extends_documentation_fragment:
    - stevefulme1.nvidia_dcgm.nvidia_common
requirements:
    - "python >= 3.9"
    - "requests"
"""

EXAMPLES = r"""
- name: Create a introspect
  stevefulme1.nvidia_dcgm.dcgm_introspect:

    state: present

- name: Delete a introspect
  stevefulme1.nvidia_dcgm.dcgm_introspect:
    name: "example-id"
    state: absent
"""

RETURN = r"""
introspect:
    description: Details of the introspect.
    returned: On success when state is present.
    type: dict
    sample:
        id: "example-id"
        name: "example-introspect"
        status: "ACTIVE"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.nvidia_dcgm.plugins.module_utils.nvidia_common import (
    NVIDIA_COMMON_ARGS,
    READY_STATES,
    DEAD_STATES,
    to_dict,
)
from ansible_collections.stevefulme1.nvidia_dcgm.plugins.module_utils.nvidia_api import (
    NvidiaApiError,
    create_api_client,
)
from ansible_collections.stevefulme1.nvidia_dcgm.plugins.module_utils.nvidia_wait import (
    wait_for_state,
)


def get_module_args():
    module_args = dict(
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )
    module_args.update(NVIDIA_COMMON_ARGS)
    return module_args


def get_resource(client, resource_id):
    """Get resource by ID."""
    try:
        return client.get(f"/v1/introspect/{resource_id}")
    except NvidiaApiError as exc:
        if exc.status == 404:
            return None
        raise


def find_resource(client, name):
    """Find resource by name."""
    if not name:
        return None
    try:
        result = client.get("/v1/introspect")
        items = result.get("data", result.get("items", []))
        for item in items:
            if item.get("status", "").upper() in DEAD_STATES:
                continue
            if item.get("name") == name:
                return item
    except NvidiaApiError:
        pass
    return None


def create_resource(module, client):
    """Create a new resource."""

    create_data = {k: v for k, v in {

    }.items() if v is not None}
    resource = client.post("/v1/introspect", data=create_data)
    if module.params.get("wait"):
        resource = wait_for_state(
            module, client,
            f"/v1/introspect/{resource.get('id', '')}",
            target_states=READY_STATES,
        )
    return resource


def update_resource(module, client, existing):
    """Update an existing resource."""

    update_data = {k: v for k, v in {

    }.items() if v is not None}
    resource = client.patch(f"/v1/introspect/{existing['id']}", data=update_data)
    if module.params.get("wait"):
        resource = wait_for_state(
            module, client,
            f"/v1/introspect/{existing['id']}",
            target_states=READY_STATES,
        )
    return resource


def delete_resource(module, client, existing):
    """Delete a resource."""
    client.delete(f"/v1/introspect/{existing['id']}")
    if module.params.get("wait"):
        wait_for_state(
            module, client,
            f"/v1/introspect/{existing['id']}",
            target_states=DEAD_STATES,
        )


def needs_update(params, existing):
    """Check if the resource needs updating."""
    updatable = []
    for attr in updatable:
        desired = params.get(attr)
        if desired is None:
            continue
        current = existing.get(attr)
        if current != desired:
            return True
    return False


def main():
    module = AnsibleModule(
        argument_spec=get_module_args(),
        supports_check_mode=True,
    )

    client = create_api_client(module)
    params = module.params

    state = params["state"]

    existing = None
    if params.get("name"):
        existing = get_resource(client, params["name"])
    elif params.get("name"):
        existing = find_resource(client, params["name"])

    if state == "absent":
        if existing is None:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        delete_resource(module, client, existing)
        module.exit_json(changed=True)
        return

    if existing is None:
        for req in []:
            if not params.get(req):
                module.fail_json(msg=f"Parameter '{req}' is required to create a introspect.")
        if module.check_mode:
            module.exit_json(changed=True)
        resource = create_resource(module, client)
        module.exit_json(changed=True, introspect=to_dict(resource))
        return

    if needs_update(params, existing):
        if module.check_mode:
            module.exit_json(changed=True)
        resource = update_resource(module, client, existing)
        module.exit_json(changed=True, introspect=to_dict(resource))
        return

    module.exit_json(changed=False, introspect=to_dict(existing))


if __name__ == "__main__":
    main()
