# Conditional Execution (`if`, `elif`, `else`)

`rconf` allows you to control the execution flow of your playbooks by running tasks only when specific conditions are met. The engine evaluates these conditions dynamically using Python.

*Note: Since conditions are evaluated as Python code, remember to wrap your string variables in single quotes (e.g., `'<< variable >>'`).*

## Simple Condition (`if`)

You can restrict a task to run only if a condition is true by using the `if` key. If the condition evaluates to false, the module is simply skipped.

**Example:**
```yaml
- name: "Determine environment"
  rconf:exec:
    run: "echo 'production'"
    save: "environment"
    show_output: false

- name: "Deploy to production"
  if: "'production' in '<< environment >>'"
  rconf:print:
    msg: "Deploying to the PRODUCTION environment!"
```

**Example with re.search:**
```yaml
- name: "Deploy to production"
  if: "re.search('prod.*', '<< environment >>')"
  rconf:print:
    msg: "Deploying to the PRODUCTION environment!"
```

---

## Complex Conditions (`if`, `elif`, `else`)

For more advanced workflows, you can use `elif` and `else` statements as fallbacks. 

**Important YAML Syntax Note:** In YAML, `elif` and `else` must be formatted as **blocks** (indented dictionaries). An `elif` block must contain its own `if` key, along with the module to execute if the condition is met.

**Example:**
```yaml
- name: "Deploy depending on the environment"
  if: "'production' in '<< environment >>'"
  rconf:print:
    msg: "Deploying to the PRODUCTION environment!"
  elif:
    if: "'stage' in '<< environment >>'"
    rconf:print:
      msg: "Deploying to the STAGING environment!"
  else:
    rconf:print:
      msg: "Not deploying to staging or production. Current environment is << environment >>"
```
