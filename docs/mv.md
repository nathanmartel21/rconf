# `mv` Module

The `rconf` `mv` module allows you to move or rename files and directories on the remote system.

## Available Parameters

The module is called via the `rconf:mv:` key in a playbook job. It requires both a source and a destination path.

* **`source`** *(required)*: The absolute path to the source file or directory you want to move.
* **`destination`** *(required)*: The absolute path to the destination where the file or directory should be moved (or its new name).
* **`perm`** *(optional)*: The octal permissions to set on the destination file or directory (e.g., `0644`).
* **`user`** *(optional)*: The system user who should own the destination.
* **`group`** *(optional)*: The system group that should own the destination.
* **`make_backup`** *(optional)*: A boolean (`true` or `false`). If `true`, creates a backup file (`.bak`) of the destination if it already exists (default: `false`).
* **`overwrite`** *(optional)*: A boolean (`true` or `false`) indicating whether to overwrite the destination if it exists (default: `true`).

---

### Basic Usage
Moves a specific file to a new location, or renames it. Overwrites the destination if it already exists.

**Example:**
```yaml
- name: "Rename configuration file"
  rconf:mv:
    source: "/etc/myapp/config.yml.new"
    destination: "/etc/myapp/config.yml"
```

---

### Move an entire directory
Moves a directory to a new location.

**Example:**
```yaml
- name: "Move web directory"
  rconf:mv:
    source: "/tmp/html_update"
    destination: "/var/www/html"
```

---

### Advanced Move with Backup
Moves a file, backs up the existing one, and changes its ownership.

**Example:**
```yaml
- name: "Deploy new executable"
  rconf:mv:
    source: "/tmp/myapp_bin"
    destination: "/usr/local/bin/myapp"
    user: "root"
    group: "root"
    perm: "0755"
    make_backup: true
```