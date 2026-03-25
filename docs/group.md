# `group` Module

The `rconf` `group` module allows you to easily manage user groups on your target systems. It seamlessly handles creating, modifying, and removing groups.

## Available Parameters

The module is called via the `rconf:group:` key in a playbook job.

* **`name`** *(required)*: The name of the group.
* **`action`** *(optional)*: `create` (default) to create or update the group, `remove` to completely delete the group.
* **`gid`** *(optional)*: The specific Group ID (GID) to assign to the group.
* **`system`** *(optional)*: A boolean (`true` or `false`, defaults to `false`). Whether the group should be created as a system group.

---

### Basic Usage
Create a standard group with default parameters.

**Example:**
```yaml
- name: "Create developers group"
  rconf:group:
    name: "developers"
    action: "create"
```

---

### Specific GID and System Group
Create a system-level group and force a specific Group ID.

**Example:**
```yaml
- name: "Create specific service group"
  rconf:group:
    name: "myapp_group"
    action: "create"
    system: true
    gid: 1050
```

---

### Removing a Group
Delete a group from the remote system.
```yaml
- name: "Remove old group"
  rconf:group:
    name: "deprecated_group"
    action: "remove"
```
