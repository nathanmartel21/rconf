# `download` Module

The `rconf` `download` module allows you to download files from HTTP, HTTPS, FTP servers, or even local sources using `file://` URIs.

It is heavily optimized for idempotency: if the file already exists at the destination, it will only be downloaded again if you specify `force: true` or if the provided `checksum` does not match the local file.

## Available Parameters

The module is called via the `rconf:download:` key in a playbook job.

* **`url`** *(required)*: The HTTP, HTTPS, FTP, or local (`file://`) URL to download.
* **`dest`** *(required)*: The absolute path where the file should be saved on the remote system (must be a file path, not a directory).
* **`checksum`** *(optional)*: Verify the downloaded file matches this checksum. If the file already exists and its checksum matches, the download is skipped. Formats accepted: `sha256:<hash>`, `md5:<hash>`, `sha1:<hash>`, `sha512:<hash>`. (If no prefix is provided, `sha256` is assumed).
* **`force`** *(optional)*: A boolean (`true` or `false`). If `true`, the file will be downloaded every time, overwriting the existing one. Defaults to `false`.
* **`extract`** *(optional)*: A boolean (`true` or `false`). If `true`, the module will attempt to extract the archive in the destination directory if it ends with `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar` or `.zip`. Defaults to `false`.
* **`username`** *(optional)*: Username for Basic Authentication.
* **`password`** *(optional)*: Password for Basic Authentication.
* **`headers`** *(optional)*: A dictionary of custom HTTP headers to pass during the request.
* **`insecure`** *(optional)*: A boolean (`true` or `false`). Skips TLS/SSL certificate validation. Defaults to `false`.
* **`timeout`** *(optional)*: The connection timeout in seconds. Defaults to `30`.
* **`perm`** *(optional)*: The octal permissions to set on the destination file (e.g., `0644`).
* **`user`** *(optional)*: The system user who should own the destination file.
* **`group`** *(optional)*: The system group that should own the destination file.

---

### Basic Usage
Downloads a single file from the internet. If `/tmp/install.sh` already exists, it will **not** be downloaded again.

**Example:**
```yaml
- name: "Download installation script"
  rconf:download:
    url: "https://example.com/install.sh"
    dest: "/tmp/install.sh"
    perm: "0755"
```

---

### Checksum Verification (Idempotent updates)
Downloads a file and verifies its SHA256 sum. If the file exists and the checksum differs, it updates the file.

**Example:**
```yaml
- name: "Download specific version of Prometheus"
  rconf:download:
    url: "https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz"
    dest: "/opt/prometheus-2.45.0.linux-amd64.tar.gz"
    checksum: "sha256:739832747120df0f10c5980753086eb2d6a5c2ceb90b16a2d1d0f50b4a69db6e"
```

---

### Bonus feature: Download & Extract
Downloads a compressed archive and extracts it immediately in the same directory.

**Example:**
```yaml
- name: "Download and extract web app source"
  rconf:download:
    url: "https://example.com/webapp-v1.zip"
    dest: "/var/www/html/webapp-v1.zip"
    extract: true
```

---

### Using Authentication and Custom Headers
Downloads a file from a private repository requiring Basic Authentication and custom HTTP Headers.

**Example:**
```yaml
- name: "Download proprietary binary"
  rconf:download:
    url: "https://api.mycompany.internal/v1/binaries/app"
    dest: "/usr/local/bin/app"
    username: "deploy_user"
    password: "SuperSecretPassword123!"
    headers:
      "Accept": "application/octet-stream"
      "X-Custom-Token": "ABC-123"
    perm: "0755"
    user: "root"
```

---

### Local file copy (`file://`)
You can use `file://` to copy files locally, benefiting from the idempotence of the checksum validation.

**Example:**
```yaml
- name: "Copy a file locally with checksum verification"
  rconf:download:
    url: "file:///mnt/nfs/shared/config.json"
    dest: "/etc/myapp/config.json"
    checksum: "md5:1c5bf08d51d5423871b96a84c7e63b65"
```