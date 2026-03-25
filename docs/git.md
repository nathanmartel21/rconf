# `git` Module

The `rconf` `git` module allows you to manage Git repositories on remote systems. It can be used to clone new repositories or to update existing ones from sources like GitHub, GitLab, or any other Git server.

## Available Parameters

The module is called via the `rconf:git:` key in a playbook job.

*   **`run`** *(optional)*: The action to perform. Can be `clone` (default), `pull`, `fetch`, or `checkout`.
*   **`repo`** *(required for `clone`)*: The URL of the repository to clone.
*   **`dest`** *(required)*: The absolute path on the remote server where the repository should be cloned or is located.
*   **`version`** *(optional)*: The branch, tag, or commit to checkout. Used by `clone`, `pull`, and `checkout`.
*   **`recursive`** *(optional)*: A boolean (`true` or `false`). If `true`, recursively clones submodules (default: `false`).
*   **`force`** *(optional)*: A boolean (`true` or `false`).
    *   For `clone`: if `true`, it will remove the destination directory if it exists before cloning.
    *   For `pull`: if `true`, it will discard local changes by resetting to the remote branch.
    *   For `checkout`: if `true`, it will discard local changes.
    *   (default: `false`).

---

### `clone`
Clones a repository. This action is idempotent and will not do anything if a repository already exists at the destination unless `force: true` is set.

**Example (cloning a specific branch):**
```yaml
- name: "Clone the project's develop branch"
  rconf:git:
    run: "clone"
    repo: "https://github.com/my-org/my-project.git"
    dest: "/var/www/my-project"
    version: "develop"
```

**Example (cloning with submodules):**
```yaml
- name: "Clone a repository and its submodules"
  rconf:git:
    run: "clone"
    repo: "https://github.com/my-org/my-app.git"
    dest: "/opt/my-app"
    recursive: true
```

---

### `pull`
Pulls the latest changes for the current branch in an existing repository.

**Example:**
```yaml
- name: "Update the project from remote"
  rconf:git:
    run: "pull"
    dest: "/var/www/my-project"
```

**Example (force pull to discard local changes):**
```yaml
- name: "Force update and discard any local changes"
  rconf:git:
    run: "pull"
    dest: "/var/www/my-project"
    version: "main"
    force: true
```

---

### `fetch`
Fetches all objects and references from all remotes.

**Example:**
```yaml
- name: "Fetch all remote changes without merging"
  rconf:git:
    run: "fetch"
    dest: "/var/www/my-project"
```

---

### `checkout`
Checks out a specific branch, tag, or commit.

**Example (deploying a specific release tag):**
```yaml
- name: "Checkout release version v1.5.0"
  rconf:git:
    run: "checkout"
    dest: "/var/www/my-project"
    version: "v1.5.0"
```
