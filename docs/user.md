# `user` Module

The `rconf` `user` module allows you to easily manage user accounts on your target systems. 

**Difference with Ansible:** Unlike Ansible which strictly requires pre-hashed passwords, `rconf` handles **plain-text passwords** safely out of the box. It securely injects the plain-text password into the system's `chpasswd` utility without leaving traces in bash history or process lists.

## Available Parameters

The module is called via the `rconf:user:` key in a playbook job.

* **`name`** *(required)*: The username of the account.
* **`action`** *(optional)*: `create` (default) to create or update the user, `remove` to completely remove the user and their home directory.
* **`password`** *(optional)*: The plain-text password to assign to the user.
* **`groups`** *(optional)*: A string or list of groups the user should belong to.
* **`append`** *(optional)*: A boolean (`true` or `false`). If `true`, append the user to the specified groups. If `false` (default), the user will be removed from groups not specified in the list.
* **`shell`** *(optional)*: The path to the user's default login shell (e.g., `/bin/bash`).
* **`home`** *(optional)*: The explicit path to the user's home directory.
* **`create_home`** *(optional)*: A boolean (`true` or `false`, defaults to `true`). Whether to create the user's home directory.
* **`system`** *(optional)*: A boolean (`true` or `false`, defaults to `false`). Whether the account should be a system account.

---

### Basic Usage
Create a standard user with default parameters.

**Example:**
```yaml
- name: "Create developer account"
  rconf:user:
    name: "jdoe"
    action: "create"
```

---

### Advanced Account Creation
Create an account with a specific password, shell, and add them to multiple groups.

**Example:**
```yaml
- name: "Create admin account"
  rconf:user:
    name: "sysadmin"
    password: "SuperSecretPassword123"
    groups: ["sudo", "docker"]
    append: true
    shell: "/bin/bash"
    action: "create"
```

---

### System and Service Accounts
Create a system user specifically for running a background service. This example sets a custom home directory without actually creating it on the disk, and appends the user to an existing group.

**Example:**
```yaml
- name: "Create background service account"
  rconf:user:
    name: "myapp_service"
    system: true
    home: "/opt/myapp"
    create_home: false
    groups: ["www-data"]
    append: true
    action: "create"
```

---

### Removing a User
Delete a user account and purge its associated home directory.
```yaml
- name: "Remove old employee account"
  rconf:user:
    name: "bsmith"
    action: "remove"
```
