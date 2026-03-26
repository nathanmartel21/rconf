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
*   **`daemon` Module**: Manage systemd services (start, stop, restart, enable, disable).
*   **`cp` Module**: Copy files and directories on remote target systems.
*   **`docker` Module**: Manage Docker containers and images (run, stop, build, pull, etc.).
*   **`dnf` Module**: Manage packages on RHEL/Fedora/CentOS-based systems.
*   **`exec` Module**: Run arbitrary shell commands (with idempotence support via creates/removes).
*   **`git` Module**: Manage Git repositories (clone, pull, fetch, etc.).
*   **`group` Module**: Create and manage user groups.
*   **`mkdir` Module**: Create and manage directories on target systems (specify paths, permissions, etc.).
*   **`mv` Module**: Move or rename files and directories on remote target systems.
*   **`ping` Module**: Check network connectivity from remote target systems
*   **`pip` Module**: Manage Python packages using the pip package manager.
*   **`print` Module**: Print messages during playbook execution (useful for debugging).
*   **`reboot` Module**: Reboot the target system.
*   **`rm` Module**: Remove files on target systems safely and idempotently.
*   **`rmdir` Module**: Remove directories on target systems safely and idempotently.
*   **`sleep` Module**: Pause playbook execution for a specified amount of time.
*   **`touch` Module**: Create and manage files on target systems (specify paths, permissions, etc.).
*   **`user` Module**: Create and manage user accounts (allows plain-text passwords natively).
*   **`whoami` Module**: A fun module to display the hostname and IP of the target system.
*   **`yum` Module**: Manage packages on older RHEL/CentOS-based systems using the YUM package manager.

## Advanced Features

`rconf` provides powerful features to create dynamic and intelligent playbooks:

*   **System Inspection (`inspect_system`)**: Automatically discover system attributes (like distribution, architecture, IP) to adapt your playbook to the target environment.
*   **Conditional Execution (`if`/`elif`/`else`)**: Control the execution flow by running tasks only when specific conditions are met.
*   **Iterations (`foreach`)**: Repeat a task multiple times over a list of items or the output of a previous command.
*   **Loops (`while`)**: Execute a task continuously until a specific condition is met, perfect for polling or waiting for a service.
