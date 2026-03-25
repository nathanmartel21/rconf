# System Inspection (`inspect_system`)

By default, `rconf` automatically inspects the target host environment when it connects. It collects essential system attributes and stores them into dynamically available variables starting with `sys_`. 

This mechanism avoids manual environment checks and allows you to write smart, cross-platform playbooks!

## Available Variables

During the inspection, the following variables are automatically populated and injected into your `<< variable >>` context:

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `<< sys_hostname >>` | The hostname of the machine. | `webserver-01` |
| `<< sys_ipv4 >>` | The main IPv4 address used to route traffic. | `192.168.1.10` |
| `<< sys_arch >>` | The architecture of the machine. | `x86_64`, `aarch64` |
| `<< sys_platform >>` | The base OS kernel platform. | `Linux` |
| `<< sys_user >>` | The user `rconf` used to log into the machine. | `root`, `natha` |
| `<< sys_distro >>` | The specific Linux distribution ID. | `ubuntu`, `centos`, `debian` |
| `<< sys_distro_version >>` | The version ID of the distribution. | `22.04`, `9` |
| `<< sys_distro_like >>` | The upstream distribution family it derives from. | `debian`, `rhel fedora` |
| `<< sys_cpu_cores >>` | The number of CPU cores available on the system. | `4`, `8` |
| `<< sys_mem_total_mb >>` | Total system RAM in Megabytes. | `8192`, `16384` |
| `<< sys_mem_free_mb >>` | Free system RAM in Megabytes. | `2048`, `4096` |
| `<< sys_disk_total_gb >>` | Total disk space of the root partition (`/`) in Gigabytes. | `20`, `100` |
| `<< sys_disk_free_gb >>` | Free disk space of the root partition (`/`) in Gigabytes. | `5`, `45` |
| `<< sys_python_version >>` | The exact Python version running on the target. | `3.10.6` |
| `<< sys_kernel_version >>` | The version of the OS kernel. | `5.15.0-76-generic` |
| `<< sys_uptime_seconds >>` | The number of seconds the system has been running. | `120456` |
| `<< sys_load_1m >>` | Load average over the last 1 minute. | `0.15` |
| `<< sys_timezone >>` | System timezone configuration. | `Europe/Paris`, `UTC` |
| `<< sys_swap_total_mb >>` | Total system swap space in Megabytes. | `2048` |
| `<< sys_swap_free_mb >>` | Free system swap space in Megabytes. | `1024` |
| `<< sys_has_docker >>` | Boolean indicating if `docker` is installed. | `True`, `False` |
| `<< sys_has_systemd >>` | Boolean indicating if `systemd` (systemctl) is present. | `True`, `False` |

---

## Example: Cross-Platform Playbook

By leveraging `sys_distro_like`, you can easily run the correct package manager depending on the host:

```yaml
- name: "Install Nginx on Debian-based systems"
  if: "'debian' in '<< sys_distro_like >>' or 'debian' == '<< sys_distro >>'"
  rconf:apt:
    run: "install"
    package: "nginx"

- name: "Install Nginx on RHEL-based systems"
  if: "'rhel' in '<< sys_distro_like >>' or 'centos' == '<< sys_distro >>'"
  rconf:dnf:
    run: "install"
    package: "nginx"
```

---

## Example: System Inspection

```yaml
- name: "Display system facts"
  rconf:print:
    color: "cyan"
    msg: |
      System Information for: << sys_hostname >> (<< sys_ipv4 >>)
      ---------------------------------------------------------
      OS Distribution : << sys_distro >> (like << sys_distro_like >>)
      Kernel Version  : << sys_kernel_version >>
      CPU Cores       : << sys_cpu_cores >>
      Memory (RAM)    : << sys_mem_free_mb >> MB free / << sys_mem_total_mb >> MB total
      Root Disk       : << sys_disk_free_gb >> GB free / << sys_disk_total_gb >> GB total
      Has Docker?     : << sys_has_docker >>
      Has Systemd?    : << sys_has_systemd >>
      Python Version  : << sys_python_version >>
```

---

## Disabling System Inspection

If you have a very large inventory and you want to speed up playbook execution, you can completely disable the system inspection by setting `inspect_system: false` at the root level of your playbook:

```yaml
inspect_system: false
targets: "web_servers"
jobs:
  # ...
```