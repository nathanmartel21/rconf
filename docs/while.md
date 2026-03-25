# `while` Loops

`rconf` supports executing tasks continuously until a specific condition is met, using the `while` keyword. This is especially useful for polling the state of a service, waiting for a file to be created, or waiting for a network resource to become available.

To prevent catastrophic infinite loops from freezing your deployment, `rconf` automatically limits the loop to a maximum of 30 iterations by default. You can override this limit using the `retry_limit` keyword.

## Basic Usage

The `while` loop re-evaluates the condition dynamically at the beginning of each iteration. Usually, this is paired with the `save` keyword to capture an output and evaluate it repeatedly.

**Example: Waiting for a file to be ready**
```yaml
- name: "Initialize output variable"
  rconf:exec:
    run: "echo 'waiting'"
    save: "check_file"
    show_output: false

- name: "Wait for a specific file to be created"
  while: "'found' not in << check_file >>"
  retry_limit: 15
  rconf:exec:
    # We sleep 2s then check if the file is ready to not spam the server
    run: "sleep 2; if [ -f /tmp/ready.txt ]; then echo 'found'; else echo 'waiting'; fi"
    save: "check_file"
    show_output: false
```

**Example: Running a task exactly 5 times**

```yaml
- name: "Ping a server 5 times with a delay"
  while: "<< while_iteration >> < 5"
  rconf:exec:
    run: "ping -c 1 8.8.8.8; sleep 1"
    show_output: true
```

**Example: Retry an unreliable command**

```yaml
- name: "Try to run a flaky command up to 10 times"
  while: "True"
  retry_limit: 10
  rconf:exec:
    run: "echo 'Trying...' && sleep 1"
    show_output: true
```

*In this example, the task will repeatedly run the command every 2 seconds until the command outputs "found" or until the loop iterates 15 times.*