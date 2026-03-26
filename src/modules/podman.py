def run(params: dict) -> str:
    """Generates podman commands based on parameters."""
    action = params.get('action', 'run')

    cmds = []

    if action == 'run':
        name = params.get('name')
        image = params.get('image')
        build_path = params.get('build_path')

        if not name:
            raise ValueError("The 'name' parameter is required for the 'run' action.")
        if not image and not build_path:
            raise ValueError("Either 'image' or 'build_path' is required for the 'run' action.")

        image_tag = image if image else name
        if build_path:
            cmds.append(f"podman build -t {image_tag} {build_path}")
        
        image_to_run = image_tag

        run_parts = ["podman run"]
        if params.get('detach', True):
            run_parts.append("-d")
        
        restart_policy = params.get('restart')
        if restart_policy:
            run_parts.append(f"--restart {restart_policy}")
        
        run_parts.append(f"--name {name}")

        for p in params.get('ports', []):
            run_parts.append(f"-p '{p}'")
        for v in params.get('volumes', []):
            run_parts.append(f"-v '{v}'")
        for k, v_val in params.get('env', {}).items():
            escaped_val = str(v_val).replace("'", "'\\''")
            run_parts.append(f"-e {k}='{escaped_val}'")
        
        run_parts.append(image_to_run)
        
        command_to_run = params.get('command')
        if command_to_run:
            run_parts.append(command_to_run)
        
        run_cmd = " ".join(run_parts)

        idempotent_script = f"""
if [ ! "$(podman ps -aq -f name=^{name}$)" ]; then
    {run_cmd}
elif [ "$(podman ps -q -f name=^{name}$ -f status=exited)" ]; then
    podman start {name}
fi
"""
        cmds.append(idempotent_script.strip().replace('\n', ' '))

    elif action == 'stop':
        name = params.get('name')
        if not name:
            raise ValueError("The 'name' parameter is required for the 'stop' action.")
        cmds.append(f"podman stop {name}")

    elif action == 'start':
        name = params.get('name')
        if not name:
            raise ValueError("The 'name' parameter is required for the 'start' action.")
        cmds.append(f"podman start {name}")

    elif action == 'remove':
        name = params.get('name')
        if not name:
            raise ValueError("The 'name' parameter is required for the 'remove' action.")
        
        force = params.get('force', False)
        remove_logic = f"podman rm -f {name}" if force else f"podman stop {name} && podman rm {name}"

        idempotent_script = f"""
if [ "$(podman ps -aq -f name=^{name}$)" ]; then
    {remove_logic}
fi
"""
        cmds.append(idempotent_script.strip().replace('\n', ' '))

    elif action == 'pull':
        image = params.get('image')
        if not image:
            raise ValueError("The 'image' parameter is required for the 'pull' action.")
        cmds.append(f"podman pull {image}")

    else:
        raise ValueError(f"Unknown action '{action}' for the podman module.")

    if not cmds:
        return "true"
        
    bash_cmd = " && ".join(cmds)
    escaped_cmd = bash_cmd.replace("'", "'\\''")
    
    return f"sudo -S bash -c '{escaped_cmd}'"