def run(params: dict) -> str:
    """Generates the git command based on parameters."""
    action = params.get('run', 'clone')
    repo = params.get('repo')
    dest = params.get('dest')
    version = params.get('version')
    recursive = params.get('recursive', False)
    force = params.get('force', False)

    if not dest:
        raise ValueError("'dest' parameter is required for the git module.")

    cmds = []

    if action == 'clone':
        if not repo:
            raise ValueError("'repo' parameter is required for the 'clone' action.")
        
        clone_cmd = "git clone"
        if recursive:
            clone_cmd += " --recursive"
        if version:
            clone_cmd += f" --branch '{version}'"
        clone_cmd += f" '{repo}' '{dest}'"
        
        if force:
            cmds.append(f"rm -rf '{dest}' && {clone_cmd}")
        else:
            # Idempotency here: only clone if the directory does not exist as a git repo
            cmds.append(f"if [ ! -d '{dest}/.git' ]; then {clone_cmd}; else exit 0; fi")

    elif action == 'pull':
        if force:
            branch_to_reset = version if version else "$(git rev-parse --abbrev-ref HEAD)"
            cmds.append(f"cd '{dest}' && git fetch origin && git reset --hard 'origin/{branch_to_reset}'")
        else:
            pull_cmd = f"git pull origin '{version}'" if version else "git pull"
            cmds.append(f"cd '{dest}' && {pull_cmd}")

    elif action == 'fetch':
        cmds.append(f"cd '{dest}' && git fetch --all --prune")
        
    elif action == 'checkout':
        if not version:
            raise ValueError("'version' parameter is required for the 'checkout' action.")
        checkout_cmd = "git checkout"
        if force:
            checkout_cmd += " -f"
        cmds.append(f"cd '{dest}' && {checkout_cmd} '{version}'")
        
    else:
        raise ValueError(f"Unknown action '{action}' for git module.")
        
    if not cmds:
        return "true"
        
    bash_cmd = " && ".join(cmds)
    escaped_cmd = bash_cmd.replace("'", "'\\''")
    
    return f"bash -c '{escaped_cmd}'"
