# Welcome to rconf Documentation

`rconf` is a configuration management and automation tool designed to manage systems efficiently. It uses simple YAML-based playbooks to define tasks and the desired state of your infrastructure.

## Playbook Structure

An `rconf` playbook consists of a list of jobs or tasks. Each task typically includes a `name` description and a module invocation (such as `rconf:apt:`), along with the module's specific parameters.

Note that all playbooks must be located in the `playbooks/` folder, and your inventory files must be placed in the `inventory/` folder.

## Running rconf

To execute a playbook against your infrastructure, use the `rconf` command line, specifying the path to the playbook and the inventory file:

```bash
rconf playbooks/main.yml -i inventory/hosts.yml
```

## Available Modules

`rconf` provides various modules to interact with and configure your target systems:

*   **`apt` Module**: Manage packages on Debian/Ubuntu-based systems (update, install, remove, purge, etc.).
*   **`mkdir` Module**: Create and manage directories on target systems (specify paths, permissions, etc.).
*   **`rmdir` Module**: Remove directories on target systems safely and idempotently.
*   **`touch` Module**: Create and manage files on target systems (specify paths, permissions, etc.).