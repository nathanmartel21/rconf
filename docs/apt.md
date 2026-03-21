# `apt` Module

The `rconf` `apt` module allows you to manage packages on Debian/Ubuntu-based systems. It provides functionalities to update the package cache, install, remove, purge, and manage packages.

## Available Actions

Each action is executed via the `rconf:apt:` key in a playbook job, with a `run` parameter specifying the action and a `package` parameter if necessary.

---

### `update`
Updates the list of available packages from the repositories.

**Example:**
```yaml
- name: "Update package cache"
  rconf:apt:
    run: "update"
```

---

### `upgrade`
Upgrades all installed packages to their latest versions.

**Exemple:**
```yaml
- name: "Upgrade the packages"
  rconf:apt:
    run: "upgrade"
```

---

### `full-upgrade`
Performs a full system upgrade, handling dependency changes.

**Exemple:**
```yaml
- name: "Complete system upgrade"
  rconf:apt:
    run: "full-upgrade"
```

---

### `install`
Installs one or more packages.

**Exemple:**
```yaml
- name: "Install Nginx"
  rconf:apt:
    run: "install"
    package: "nginx"
```

**Example (install multiple packages):**
```yaml
- name: "Install Nginx, Git and Chrony"
  rconf:apt:
    run: "install"
    package: "nginx git chrony"
```

---

### `remove`
Removes one or more packages, but keeps configuration files.

**Exemple:**
```yaml
- name: "Remove Nginx"
  rconf:apt:
    run: "remove"
    package: "nginx"
```

---

### `purge`
Removes one or more packages along with their configuration files.

**Exemple:**
```yaml
- name: "Purge Nginx"
  rconf:apt:
    run: "purge"
    package: "nginx"
```

---

### `reinstall`
Reinstalls an existing package.

**Exemple:**
```yaml
- name: "Reinstall Apache2"
  rconf:apt:
    run: "reinstall"
    package: "apache2"
```

---

### `autoremove`
Removes packages that were automatically installed to satisfy dependencies and are no longer needed.

**Exemple:**
```yaml
- name: "Clean up unused dependencies"
  rconf:apt:
    run: "autoremove"
```

---

### `clean`
Cleans the cache of downloaded packages (`.deb`).

**Exemple:**
```yaml
- name: "Clean the APT cache"
  rconf:apt:
    run: "clean"
```

---

### `autoclean`
Cleans the cache of downloaded packages, but only removes packages that can no longer be downloaded and are therefore useless.

**Exemple:**
```yaml
- name: "Clear the APT cache (automatic)"
  rconf:apt:
    run: "autoclean"
```

---

### `list`
Lists packages. Can be filtered by a package name.

**Example (list all packages):**
```yaml
- name: "List all packages"
  rconf:apt:
    run: "list"

# Example (list a specific package):

- name: "List Nginx package"
  rconf:apt:
    run: "list"
    package: "nginx"
```

---

### `search`
Searches for a package by its name or description.

**Exemple:**
```yaml
- name: "Search for a package"
  rconf:apt:
    run: "search"
    package: "php"
```

---

### `show`
Displays details of a package.

**Exemple:**
```yaml
- name: "Show Nginx details"
  rconf:apt:
    run: "show"
    package: "nginx"
```

---

### `satisfy`
Attempts to satisfy complex dependencies.

**Exemple:**
```yaml
- name: "Satisfying an dependencies"
  rconf:apt:
    run: "satisfy"
    package: "libssl-dev (>= 1.1.1)"
```

---

### `edit-sources`
Opens the APT sources configuration file in a text editor. **Warning:** This command is interactive and may block execution if used in a non-interactive context.

**Exemple:**
```yaml
- name: "Edit APT source code"
  rconf:apt:
    run: "edit-sources"
```
