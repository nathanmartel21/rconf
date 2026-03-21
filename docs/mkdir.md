# `mkdir` Module

The `rconf` `mkdir` module allows you to safely create directories on remote systems. It is idempotent, meaning it will verify the current state of the directory and only apply changes if necessary.

## Available Parameters

The module is called via the `rconf:mkdir:` key in a playbook job. It requires a path and accepts optional parameters for permissions and ownership.

* **`path`** *(required)*: The absolute path to the directory you want to create.
* **`perm`** *(optional)*: The octal permissions to set on the directory (default: `0755`).
* **`user`** *(optional)*: The system user who should own the directory.
* **`group`** *(optional)*: The system group that should own the directory.

---

### Basic Usage
Ensures a directory exists. If it does not exist, it will be created with default permissions (`0755`) and root ownership (since rconf uses sudo).

**Example:**
```yaml
- name: "Ensure config directory exists"
  rconf:mkdir:
    path: "/etc/myapp"
```

---

### Custom Permissions and Ownership
Ensures a directory exists with a specific owner, group, and strict permissions.

**Example:**
```yaml
- name: "Create a secure data folder for postgres"
  rconf:mkdir:
    path: "/var/lib/pgsql/data"
    perm: "0700"
    user: "postgres"
    group: "postgres"
```