# `print` Module

The `rconf` `print` module allows you to print messages during playbook execution, similar to the `debug` module in Ansible. It is highly useful for debugging purposes or displaying information to the user during a run.

## Available Parameters

The module is called via the `rconf:print:` key in a playbook job. It requires a message to print.

* **`msg`** *(required)*: The message string you want to display.
* **`color`** *(optional)*: The color for the local console output (`green`, `red`, `yellow`, `cyan`, `magenta`).
* **`file`** *(optional)*: The absolute path to a file on the remote system to append the message to.

---

### Basic Usage
Prints a simple text message to the console during the playbook run.

**Example:**
```yaml
- name: "Display a debug message"
  rconf:print:
    msg: "The application configuration has been successfully updated."
```