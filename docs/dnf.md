# `dnf` Module

The `rconf` `dnf` module allows you to manage packages on RHEL, Fedora, CentOS, and other systems using the DNF package manager. It provides functionalities to update the package cache, install, remove, and manage packages.

## Available Actions

Each action is executed via the `rconf:dnf:` key in a playbook job, with a `run` parameter specifying the action and a `package` parameter if necessary.

---

### `update` or `makecache`
Updates the list of available packages from the repositories (generates the metadata cache).

**Example:**
```yaml
- name: "Update package cache"
  rconf:dnf:
    run: "update"
```

---

### `check-update`
Checks if there are updates available for your system without actually installing them.

**Example:**
```yaml
- name: "Check for updates"
  rconf:dnf:
    run: "check-update"
```

---

### `upgrade`
Upgrades all installed packages to their latest versions.

**Example:**
```yaml
- name: "Upgrade the packages"
  rconf:dnf:
    run: "upgrade"
```

---

### `full-upgrade` or `distro-sync`
Performs a full system upgrade, synchronizing installed packages to the latest available versions.

**Example:**
```yaml
- name: "Complete system upgrade"
  rconf:dnf:
    run: "distro-sync"
```

---

### `install`
Installs one or more packages.

**Example:**
```yaml
- name: "Install Nginx"
  rconf:dnf:
    run: "install"
    package: "nginx"
```

**Example (install multiple packages):**
```yaml
- name: "Install Nginx, Git and Chrony"
  rconf:dnf:
    run: "install"
    package: "nginx git chrony"
```

---

### `remove`
Removes one or more packages.

**Example:**
```yaml
- name: "Remove Nginx"
  rconf:dnf:
    run: "remove"
    package: "nginx"
```

---

### `purge`
For DNF, this acts as an alias to `remove` to maintain compatibility with `apt` playbooks.

**Example:**
```yaml
- name: "Purge Nginx"
  rconf:dnf:
    run: "purge"
    package: "nginx"
```

---

### `reinstall`
Reinstalls an existing package.

**Example:**
```yaml
- name: "Reinstall Nginx"
  rconf:dnf:
    run: "reinstall"
    package: "nginx"
```

---

### `downgrade`
Downgrades a package to an older version.

**Example:**
```yaml
- name: "Downgrade a package"
  rconf:dnf:
    run: "downgrade"
    package: "nginx"
```

---

### `autoremove`
Removes packages that were automatically installed to satisfy dependencies and are no longer needed.

**Example:**
```yaml
- name: "Clean up unused dependencies"
  rconf:dnf:
    run: "autoremove"
```

---

### `clean`
Cleans all DNF cached files (`clean all`).

**Example:**
```yaml
- name: "Clean the DNF cache"
  rconf:dnf:
    run: "clean"
```

---

### `autoclean`
Cleans the cache of downloaded packages (`clean packages`).

**Example:**
```yaml
- name: "Clear the DNF package cache"
  rconf:dnf:
    run: "autoclean"
```

---

### `list`
Lists packages. Can be filtered by a package name.

**Example (list all packages):**
```yaml
- name: "List all packages"
  rconf:dnf:
    run: "list"

# Example (list a specific package):

- name: "List Nginx package"
  rconf:dnf:
    run: "list"
    package: "nginx"
```

---

### `search`
Searches for a package by its name or description.

**Example:**
```yaml
- name: "Search for a package"
  rconf:dnf:
    run: "search"
    package: "php"
```

---

### `show` or `info`
Displays details of a package.

**Example:**
```yaml
- name: "Show Nginx details"
  rconf:dnf:
    run: "info"
    package: "nginx"
```