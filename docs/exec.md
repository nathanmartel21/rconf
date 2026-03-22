# `exec` Module

The `rconf` `exec` module allows you to run arbitrary shell commands on your remote target systems.

By using the `creates` or `removes` parameters, you can make your commands idempotent, ensuring they only run when strictly necessary.

## Available Parameters

The module is called via the `rconf:exec:` key in a playbook job.

* **`run`** *(required)*: The shell command you want to execute.
* **`chdir`** *(optional)*: Change into this directory before running the command.
* **`creates`** *(optional)*: A filename; if it already exists, this step won't be run (useful for idempotence).
* **`removes`** *(optional)*: A filename; if it does not exist, this step won't be run (useful for idempotence).
* **`show_output`** *(optional)*: A boolean (`true` or `false`). If set to `true`, the standard output of the command will be printed in the console (useful for commands like `df -h`).

---

### Basic Usage
Execute a simple shell command.

**Example:**
```yaml
- name: "Update a specific database"
  rconf:exec:
    run: "mysql -u root < /tmp/update.sql"
```

---

### Execute in a specific directory
Run a script located in a specific directory.

**Example:**
```yaml
- name: "Run the build script"
  rconf:exec:
    run: "./build.sh"
    chdir: "/opt/myapp/source"
```

---

### Idempotent Execution
Download a file only if it hasn't been downloaded yet.
```yaml
- name: "Download node_exporter"
  rconf:exec:
    run: "wget https://example.com/node_exporter.tar.gz"
    chdir: "/tmp"
    creates: "/tmp/node_exporter.tar.gz"
```