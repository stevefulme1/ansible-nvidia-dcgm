    # stevefulme1.nvidia_dcgm

    Ansible Collection for NVIDIA DCGM (Data Center GPU Manager). Provides modules for managing GPU groups, field groups, policies, health checks, diagnostics, and Prometheus exporter setup.

    ## Requirements

    - Ansible >= 2.16
    - Python >= 3.9
    - `requests` Python library

    ## Modules

    - `stevefulme1.nvidia_dcgm.dcgm_group` - Manage DCGM GPU groups
- `stevefulme1.nvidia_dcgm.dcgm_group_info` - Retrieve DCGM group details
- `stevefulme1.nvidia_dcgm.dcgm_field_group` - Manage DCGM field groups
- `stevefulme1.nvidia_dcgm.dcgm_field_group_info` - Retrieve DCGM field group details
- `stevefulme1.nvidia_dcgm.dcgm_policy` - Manage DCGM policies
- `stevefulme1.nvidia_dcgm.dcgm_policy_info` - Retrieve DCGM policy details
- `stevefulme1.nvidia_dcgm.dcgm_health_check` - Run DCGM GPU health checks
- `stevefulme1.nvidia_dcgm.dcgm_diagnostics` - Run DCGM GPU diagnostics
- `stevefulme1.nvidia_dcgm.dcgm_stats` - Retrieve DCGM GPU statistics
- `stevefulme1.nvidia_dcgm.dcgm_config` - Manage DCGM configurations
- `stevefulme1.nvidia_dcgm.dcgm_config_info` - Retrieve DCGM configuration details
- `stevefulme1.nvidia_dcgm.dcgm_introspect` - Retrieve DCGM introspection data

    ## Roles

    - `dcgm_install` - Install NVIDIA DCGM on target hosts
- `dcgm_exporter` - Set up DCGM Prometheus exporter

    ## EDA

    - `dcgm_alerts` - Watch DCGM for GPU health alerts

    ## License

    GPL-3.0-or-later
