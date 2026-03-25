# `whoami` Module

The `rconf` `whoami` module is a fun utility to confirm the identity of the remote host you are running the playbook on.

It displays the hostname and primary IP address of the target machine, announced by a friendly ASCII art ghost. It's a great way to visually confirm which machine you're working on.

This module does not take any parameters. For the output to be visible, you must set `show_output: true`.

---

### Basic Usage

**Example Playbook:**
```yaml
- name: "Who is this host?"
  rconf:whoami:
    show_output: true
```

**Example Output:**
```
 ---------------------------------------
< Wooo! I'm webserver-01 (192.168.1.55) >
 ---------------------------------------
         \   
          \  .-.
            (o o)
            | O \
             \   \
              `~~~
```