# `docker` Module

The `rconf` `docker` module allows you to manage Docker containers and images on remote systems. It provides functionalities to run, stop, and remove containers, as well as pull or build images.

## Available Parameters

*   **`action`** *(optional)*: The action to perform. The default value is `run`. Valid values:
    *   `run`: Ensures a container is running. Creates it from an image if it doesn't exist, or starts it if stopped. This is the default action.
    *   `stop`: Stops a running container.
    *   `start`: Starts a stopped container.
    *   `remove`: Stops and removes a container.
    *   `pull`: Downloads an image from a registry.
*   **`name`**: The name of the container. Required for most actions.
*   **`image`**: The image to use (e.g., `nginx:latest`). Required for `run` (unless `build_path` is used) and `pull`.
*   **`build_path`**: Path to a directory containing a `Dockerfile`. If provided with `action: run`, an image will be built and tagged with the value of the `image` parameter (or `name` if `image` is not set), then the container will be started from it.
*   **`ports`**: A list of port mappings (e.g., `["80:80", "443:443"]`).
*   **`volumes`**: A list of volume mappings (e.g., `["/data:/var/lib/mysql"]`).
*   **`env`**: A dictionary of environment variables.
*   **`restart`**: Restart policy for the container (e.g., `always`).
*   **`command`**: Command to execute in the container.
*   **`force`**: For `action: remove`, forces the removal of the container (`docker rm -f`). Defaults to `false`.
*   **`detach`**: Runs the container in the background. Defaults to `true`.

---

### Run a container

Ensures a container named `my-nginx` is running, based on the `nginx:alpine` image, with a port mapping.

**Example:**
```yaml
- name: "Run an Nginx container"
  rconf:docker:
    name: "my-nginx"
    image: "nginx:alpine"
    ports:
      - "8080:80"
```

---

### Build and run a container

Builds a Docker image from a local path, then runs a container from that image.

**Example:**
```yaml
- name: "Build and run a custom web application"
  rconf:docker:
    action: run
    name: "my-web-app"
    build_path: "/home/user/app/src"
    image: "custom-app:1.0" # The tag for the built image
    ports:
      - "3000:3000"
```

---

### Stop and remove a container

Ensures a container is stopped and removed from the host.

**Example:**
```yaml
- name: "Remove the old database container"
  rconf:docker:
    action: "remove"
    name: "old-db"
```

---

### Pull an image

Ensures a specific Docker image is pulled onto the host.

**Example:**
```yaml
- name: "Pull the latest Redis image"
  rconf:docker:
    action: "pull"
    image: "redis:latest"
```
