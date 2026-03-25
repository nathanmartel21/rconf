# `pip` Module

The `rconf` `pip` module allows you to manage Python packages using the pip package manager. It supports installing, removing, and inspecting packages. 

By default, this module uses the `pip3` executable without `sudo`. You can easily target a specific virtual environment by overriding the `executable` parameter.

## Available Actions

Each action is executed via the `rconf:pip:` key in a playbook job, with a `run` parameter specifying the action and a `package` parameter if necessary.

---

### `install`
Installs one or more Python packages.

**Example:**
```yaml
- name: "Install requests"
  rconf:pip:
    run: "install"
    package: "requests"
```

**Example (install in a specific virtual environment):**
```yaml
- name: "Install Flask in venv"
  rconf:pip:
    run: "install"
    package: "Flask"
    executable: "/var/www/myapp/venv/bin/pip"
```

**Example (upgrade a package):**
```yaml
- name: "Upgrade pip itself"
  rconf:pip:
    run: "install"
    package: "--upgrade pip"
```

---

### `remove` or `uninstall`
Uninstalls one or more Python packages automatically (bypasses the confirmation prompt).

**Example:**
```yaml
- name: "Remove requests"
  rconf:pip:
    run: "uninstall"
    package: "requests"
```

---

### `list`
Lists all installed Python packages.

**Example:**
```yaml
- name: "List installed packages"
  rconf:pip:
    run: "list"
```

---

### `freeze`
Outputs installed packages in requirements format (useful combined with the `save` keyword).

**Example:**
```yaml
- name: "Freeze packages"
  rconf:pip:
    run: "freeze"
```

---

### `show`
Shows detailed information about one or more installed packages.

**Example:**
```yaml
- name: "Show requests info"
  rconf:pip:
    run: "show"
    package: "requests"
```

---

### `check`
Verifies that installed packages have compatible dependencies.

**Example:**
```yaml
- name: "Check dependencies"
  rconf:pip:
    run: "check"
```

---

### `clean`
Inspects and manages pip's wheel cache by purging it (`pip cache purge`).

**Example:**
```yaml
- name: "Clean pip cache"
  rconf:pip:
    run: "clean"
```