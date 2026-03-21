# `touch` Module

The `rconf` `touch` module allows you to safely create empty files on remote systems or update their permissions/ownership. It is idempotent, meaning it will verify the current state of the file and only apply changes if necessary.

## Available Parameters

The module is called via the `rconf:touch:` key in a playbook job. It requires a path and accepts optional parameters for permissions and ownership.

* **`path`** *(required)*: The absolute path to the file you want to create.
* **`perm`** *(optional)*: The octal permissions to set on the file (default: `0644`).
* **`user`** *(optional)*: The system user who should own the file.
* **`group`** *(optional)*: The system group that should own the file.

---

### Basic Usage
Ensures a file exists. If it does not exist, it will be created as an empty file with default permissions (`0644`).

**Example:**
```yaml
- name: "Ensure lock file exists"
  rconf:touch:
    path: "/var/run/myapp.lock"
```

---

### Custom Permissions and Ownership
Ensures a file exists with specific ownership and restrictive permissions.

**Example:**
```yaml
- name: "Create a secure credentials file"
  rconf:touch:
    path: "/etc/myapp/credentials.json"
    perm: "0600"
    user: "myapp_user"
    group: "myapp_group"
```