# `tar` Module

The `rconf` `tar` module allows you to **compress** and **extract** archives on your remote target systems. It supports the most common archive formats.

## Available Parameters

The module is called via the `rconf:tar:` key in a playbook job.

### General Parameters

* **`action`** *(optional)*: Either `extract` (default) or `compress`.

---

### Extract Mode (`action: extract`)

* **`src`** *(required)*: Path to the source archive file on the remote host.
* **`dest`** *(optional)*: Destination directory where the archive should be extracted. If omitted, the directory containing the archive is used.
* **`strip`** *(optional)*: Number of leading path components to strip during extraction (`--strip-components`).
* **`format`** *(optional)*: Explicit archive format. Auto-detected from the file extension if omitted. Supported values: `tar`, `gz`, `bz2`, `xz`, `zst`.
* **`force`** *(optional)*: Boolean (`true` or `false`). If `true`, the destination directory is removed *before* extraction.
* **`overwrite`** *(optional)*: Boolean. If `true`, existing files in the destination are overwritten without clearing the entire directory first. Defaults to `false`.
* **`keep_newer`** *(optional)*: Boolean. If `true`, do not overwrite existing files that are newer than the archive contents (`--keep-newer-files`). Defaults to `false`.
* **`exclude`** *(optional)*: A pattern (string) or a list of patterns to exclude from extraction (`--exclude`).
* **`perm`** *(optional)*: Permissions to set on the extracted tree (`chmod -R`).
* **`user`** *(optional)*: Owner to set on the extracted tree (`chown -R`).
* **`group`** *(optional)*: Group to set on the extracted tree (`chgrp -R`).

### Compress Mode (`action: compress`)

* **`src`** *(required)*: Path to the file or directory to compress.
* **`dest`** *(required)*: Destination archive path (e.g., `/tmp/backup.tar.gz`).
* **`format`** *(optional)*: Compression format. Auto-detected from the destination extension if omitted. Supported values: `tar`, `gz`, `bz2`, `xz`, `zst`.
* **`exclude`** *(optional)*: A pattern (string) or a list of patterns to exclude from the archive (`--exclude`).
* **`transform`** *(optional)*: Sed transformation expression (`--transform`) applied to file names inside the archive (e.g., `s|^/opt/app|app|`).
* **`dereference`** *(optional)*: Boolean. If `true`, follow symlinks and archive the files they point to. Defaults to `false`.

---

## Basic Usage — Extract an archive

Extracts a `.tar.gz` archive to a specified directory.

```yaml
- name: "Extract application archive"
  rconf:tar:
    src: "/tmp/app-v1.2.3.tar.gz"
    dest: "/opt/app"
```

---

## Extract with path stripping

Removes the first directory component from the archive paths.

```yaml
- name: "Extract with strip-components"
  rconf:tar:
    src: "/tmp/node_exporter-1.6.0.linux-amd64.tar.gz"
    dest: "/opt/node_exporter"
    strip: 1
```

---

## Force clean extraction

Removes the destination directory before extracting — useful for clean deployments.

```yaml
- name: "Clean extraction of webapp"
  rconf:tar:
    src: "/tmp/webapp.tar.gz"
    dest: "/var/www/html"
    force: true
```

---

## Extract with permissions and ownership

Sets permissions and ownership on all extracted files.

```yaml
- name: "Extract vendor assets"
  rconf:tar:
    src: "/tmp/assets.tar.bz2"
    dest: "/var/www/assets"
    perm: "0644"
    user: "www-data"
    group: "www-data"
```

---

## Compress a directory

Creates a `.tar.gz` archive of a directory.

```yaml
- name: "Backup application logs"
  rconf:tar:
    action: compress
    src: "/var/log/myapp"
    dest: "/backups/myapp-logs-20250322.tar.gz"
```

---

## Compress with exclusion

Creates an archive while skipping certain files or directories.

```yaml
- name: "Backup project with exclusions"
  rconf:tar:
    action: compress
    src: "/opt/myproject"
    dest: "/tmp/myproject.tar.gz"
    exclude:
      - "node_modules"
      - ".git"
      - "*.log"
```

---

## Compress with transformation

Creates an archive where file paths are rewritten using a sed expression.

```yaml
- name: "Create relocatable archive"
  rconf:tar:
    action: compress
    src: "/opt/myapp"
    dest: "/tmp/myapp.tar.gz"
    transform: "s|^/opt/myapp/||"
```

---

## Extract a zip file

The module also handles `.zip` archives transparently via `unzip`.

```yaml
- name: "Extract zip archive"
  rconf:tar:
    src: "/tmp/data.zip"
    dest: "/opt/data"
```

---

## Auto-detection of format

If you don't specify `format`, the module analyses the file extension (`*.tar.gz`, `*.tgz`, `*.tar.bz2`, `*.tbz2`, `*.tar.xz`, `*.txz`, `*.tar.zst`, `*.tar`, `*.zip`) and selects the appropriate extraction or compression tool.

```yaml
- name: "Extract — format auto-detected"
  rconf:tar:
    src: "/tmp/backup.tar.xz"
    dest: "/opt/restore"
```