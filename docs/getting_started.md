# Getting Started with stevefulme1.nvidia_dcgm

>-

## Installation

```bash
ansible-galaxy collection install stevefulme1.nvidia_dcgm
```

## Requirements

- Ansible >= 2.16
- Python >= 3.12

## Authentication

Refer to individual module documentation for authentication requirements.

## Quick Example

```yaml
---
- name: Example playbook
  hosts: localhost
  connection: local
  gather_facts: false
  collections:
    - stevefulme1.nvidia_dcgm
  tasks:
    - name: Get info
      stevefulme1.nvidia_dcgm.dcgm_config:
        api_url: "{{ api_url }}"
        api_token: "{{ api_token }}"
      register: result

    - name: Show result
      ansible.builtin.debug:
        var: result
```

## Collection Contents

- **Modules**: 12
- **Roles**: 2
- **EDA plugins**: 1

## Next Steps

- Browse the module documentation: `ansible-doc stevefulme1.nvidia_dcgm.<module_name>`
- Check the [README](../README.md) for the full module and role list
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute
