# -*- coding: utf-8 -*-
# Copyright (c) 2024, Steve Fulmer
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for retrieve dcgm field group details."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dcgm_field_group_info
short_description: Retrieve DCGM field group details
description:
    - Retrieve DCGM field group details using the NVIDIA REST API.
    - This module requires the C(requests) Python library.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    field_group_id:
        description:
            - The field group id for the field group.
        type: str
    name:
        description:
            - The name for the field group.
        type: str
extends_documentation_fragment:
    - stevefulme1.nvidia_dcgm.nvidia_common
requirements:
    - "python >= 3.9"
    - "requests"
"""

EXAMPLES = r"""
- name: Get field group details
  stevefulme1.nvidia_dcgm.dcgm_field_group_info:
    field_group_id: "example-id"
"""

RETURN = r"""
field_group:
    description: Details of the field group.
    returned: On success.
    type: dict
    sample:
        id: "example-id"
        name: "example-field_group"
        status: "ACTIVE"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.nvidia_dcgm.plugins.module_utils.nvidia_common import (
    NVIDIA_COMMON_ARGS,
    to_dict,
)
from ansible_collections.stevefulme1.nvidia_dcgm.plugins.module_utils.nvidia_api import (
    NvidiaApiError,
    create_api_client,
)


def get_module_args():
    module_args = dict(
        field_group_id=dict(type="str"),
        name=dict(type="str"),
    )
    module_args.update(NVIDIA_COMMON_ARGS)
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=get_module_args(),
        supports_check_mode=True,
    )

    client = create_api_client(module)
    params = module.params

    if params.get("field_group_id"):
        try:
            resource = client.get(f"/v1/field_groups/{params['field_group_id']}")
            module.exit_json(changed=False, field_group=to_dict(resource))
        except NvidiaApiError as exc:
            if exc.status == 404:
                module.exit_json(changed=False, field_group={})
            module.fail_json(msg=str(exc))
    else:
        try:
            result = client.get("/v1/field_groups")
            items = result.get("data", result.get("items", []))
            module.exit_json(changed=False, field_groups=[to_dict(i) for i in items])
        except NvidiaApiError as exc:
            module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
