# `reboot` Module

The `rconf` `reboot` module allows you to reboot the remote target system. It leverages the standard `shutdown -r` command.

> **Note**: Rebooting a machine immediately (`delay: "now"`) might cause the `rconf` SSH connection to drop abruptly, which could occasionally result in a connection error output in your console (even if the system is successfully rebooting). Scheduling it 1 minute in advance prevents this.

## Available Parameters

The module is called via the `rconf:reboot:` key in a playbook job.

* **`delay`** *(optional)*: The time to wait before rebooting. Can be `now` (default), an integer representing minutes (e.g., `5`), or a specific time (e.g., `23:00`).
* **`msg`** *(optional)*: A warning message to broadcast to all logged-in users before the system goes down.

---

### Basic Usage
Reboots the machine immediately.

**Example:**
```yaml
- name: "Reboot the server immediately"
  rconf:reboot: {}
```

---

### Delayed Reboot with Message
Schedules a reboot in 5 minutes and broadcasts a custom warning message to users.

**Example:**
```yaml
- name: "Schedule reboot after updates"
  rconf:reboot:
    delay: 5
    msg: "System will reboot in 5 minutes for kernel updates."
```