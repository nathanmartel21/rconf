# `rm` Module

The `rconf` `rm` module allows you to safely remove files on remote systems. It is idempotent, meaning it will not fail if the file has already been removed. It includes basic protection against removing the root directory.

## Available Parameters

The module is called via the `rconf:rm:` key in a playbook job. It requires a path.

* **`path`** *(required)*: The absolute path to the file you want to remove.

---

### Basic Usage
Removes a specific file. If the file does not exist, the task succeeds without error.

**Example:**
```yaml
- name: "Remove temporary config file"
  rconf:rm:
    path: "/tmp/old_config.tmp"
```