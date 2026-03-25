# `sleep` Module

The `rconf` `sleep` module allows you to pause the execution of your playbook for a specific number of seconds. This is especially useful when you need to wait for a service to fully start or for a background process to complete before moving on to the next task.

## Available Parameters

The module is called via the `rconf:sleep:` key in a playbook job.

* **`seconds`** *(required)*: The number of seconds to wait. Must be an integer.

---

### Basic Usage
Pauses the playbook execution for 10 seconds.

**Example:**
```yaml
- name: "Start the application service"
  rconf:exec:
    run: "systemctl start my_app"

- name: "Wait for the service to initialize"
  rconf:sleep:
    seconds: 10
```