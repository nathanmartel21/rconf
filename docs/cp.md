# `cp` Module

The `rconf` `cp` module allows you to copy files and directories directly on the remote system.

## Available Parameters

The module is called via the `rconf:cp:` key in a playbook job. It requires both a source and a destination path.

* **`src`** *(required)*: The absolute path to the source file or directory you want to copy.
* **`dest`** *(required)*: The absolute path to the destination where the file or directory should be copied.
* **`recursive`** *(optional)*: A boolean (`true` or `false`) indicating whether to copy directories recursively (default: `false`).

---

### Basic Usage
Copies a specific file to a new location. Overwrites the destination if it already exists.

**Example:**
```yaml
- name: "Copy configuration file"
  rconf:cp:
    src: "/etc/myapp/default_config.yml"
    dest: "/etc/myapp/config.yml"
```

---

### Recursive Copy
Copies an entire directory and its contents to a new location (equivalent to `cp -r`).

**Example:**
```yaml
- name: "Backup web directory"
  rconf:cp:
    src: "/var/www/html"
    dest: "/var/www/html_backup"
    recursive: true
```