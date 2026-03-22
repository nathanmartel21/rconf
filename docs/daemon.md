# `daemon` Module

The `rconf` `daemon` module allows you to manage systemd services on remote systems. It provides functionalities to start, stop, restart, or reload services, as well as enabling or disabling them to start at boot.

## Available Parameters

The module is called via the `rconf:daemon:` key in a playbook job. It requires the name of the service to manage.

* **`name`** *(required)*: The name of the service (e.g., `nginx`, `docker`).
* **`state`** *(optional)*: The desired state of the service. Valid values are `started`, `stopped`, `restarted`, and `reloaded`.
* **`enabled`** *(optional)*: A boolean (`true` or `false`) indicating whether the service should start on boot.

---

### Basic Usage
Starts a service.

**Example:**
```yaml
- name: "Start the Nginx service"
  rconf:daemon:
    name: "nginx"
    state: "started"
```

---

### Enable and Start
Ensures a service is enabled to start on system boot and is currently running.

**Example:**
```yaml
- name: "Enable and start Docker"
  rconf:daemon:
    name: "docker"
    status: "started"
    enabled: true
```

---

### Stop and Disable
Stops a service and prevents it from starting on system boot.

**Example:**
```yaml
  rconf:daemon:
    name: "apache2"
    status: "stopped"
    enabled: false
```