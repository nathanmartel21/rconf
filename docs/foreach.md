# Iterations (`foreach`)

`rconf` supports iterating over lists or dynamic variables to repeat a task multiple times efficiently. During execution, the current iteration value is injected into the context and is accessible via the `<< value >>` variable. You can use the `foreach` keyword for this.

## 1. Simple List Loop
You can iterate through a straightforward list of strings or numbers.

**Example:**
```yaml
- name: "Create essential groups"
  foreach:
    - "developers"
    - "sysadmins"
    - "database_admins"
  rconf:group:
    name: "<< value >>"
    action: "create"
```

## 2. Advanced Loop with Dictionaries
If you provide a list of dictionaries, `rconf` intelligently maps each key to an value property, prefixed by `value_`. For instance, `{ user: "john", shell: "/bin/zsh" }` creates `<< value_user >>` and `<< value_shell >>`.

**Example:**
```yaml
- name: "Create customized user accounts"
  foreach:
    - { username: "alice", shell: "/bin/bash", group: "developers" }
    - { username: "bob", shell: "/bin/zsh", group: "sysadmins" }
  rconf:user:
    name: "<< value_username >>"
    login_shell: "<< value_shell >>"
    member_of: "<< value_group >>"
    action: "create"
```

## 3. Dynamic Loop (Iterating over Output)
You can capture the multiline output of a command (using the `save` keyword) and loop over each line dynamically.

**Example:**
```yaml
- name: "List all files in temporary directory"
  rconf:exec:
    run: "ls -1 /tmp/configs/"
    save: "config_files"
    show_output: false
    
- name: "Process each configuration file"
  foreach: "<< config_files >>"
  rconf:print:
    msg: "Processing the configuration file: << value >>"
```