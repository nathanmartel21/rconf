# `rmdir` Module

The `rconf` `rmdir` module allows you to safely remove directories on remote systems. It is idempotent, meaning it will not fail if the directory has already been removed. It also includes basic protection to prevent accidental deletion of the root directory (`/`).

## Available Parameters

The module is called via the `rconf:rmdir:` key in a playbook job. It requires a path and accepts an optional parameter for recursive deletion.

* **`path`** *(required)*: The absolute path to the directory you want to remove.
* **`recursive`** *(optional)*: A boolean (`true` or `false`) indicating whether to remove the directory and its contents recursively (default: `false`).

---

### Basic Usage
Removes a directory only if it is empty. If the directory does not exist, the task succeeds without error.

**Example:**
```yaml
- name: "Remove temporary config directory"
  rconf:rmdir:
    path: "/etc/myapp/temp"
```

---

### Recursive Removal
Removes a directory and all of its contents (equivalent to `rm -rf`).

**Example:**
```yaml
- name: "Remove entire app folder"
  rconf:rmdir:
    path: "/opt/old_app"
    recursive: true
```