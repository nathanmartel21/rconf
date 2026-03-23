# `ping` Module

The `rconf` `ping` module allows you to check network connectivity to one or multiple hosts from the remote target system. It executes a single ICMP echo request (`ping -c 1`) per host and filters the output to display only the essential connectivity statistics while maintaining the correct exit code. If checking multiple hosts, the task will fail if any of the hosts is unreachable.

## Available Parameters

The module is called via the `rconf:ping:` key in a playbook job. It requires a `host` to ping.

* **`host`** *(required)*: The IP address or hostname you want to ping. Can be a single string or a list of strings for multiple hosts.
* **`show_output`** *(optional)*: A boolean (`true` or `false`). If set to `true`, the filtered standard output of the ping command will be printed in the console.

---

### Basic Usage
Checks connectivity to a host. If the host is unreachable, the task will fail.

**Example:**
```yaml
- name: "Check connectivity to Google DNS"
  rconf:ping:
    host: "8.8.8.8"
```

---

### Displaying Output
Pings a host and displays the filtered result in the console.

**Example:**
```yaml
- name: "Check connectivity to local router"
  rconf:ping:
    host: "192.168.1.1"
    show_output: true
```

---

### Pinging Multiple Hosts
You can provide a list of hosts to check connectivity to several destinations at once.

**Example:**
```yaml
- name: "Check connectivity to multiple DNS servers"
  rconf:ping:
    host:
      - "8.8.8.8"
      - "1.1.1.1"
    show_output: true
```
```