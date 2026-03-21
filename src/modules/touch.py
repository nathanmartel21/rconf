import base64
import json

def run(params: dict) -> str:
    """
    Generates a shell command string to execute the touch logic on the remote host.
    """
    path = params.get('path')
    perm = params.get('perm', '0644')
    user = params.get('user')
    group = params.get('group')

    if not path:
        raise ValueError("The 'path' parameter is required for rconf:touch")

    python_script_template = """
import os, sys, json, pwd, grp

def _execute_remote_touch_logic(path, perm='0644', user=None, group=None):
    if not path:
        return {{"failed": True, "msg": "The 'path' parameter is required."}}
    changed = False
    msg_parts = []
    try:
        if not os.path.exists(path):
            open(path, 'a').close()
            changed = True
            msg_parts.append(f"File '{{path}}' was successfully created.")
        else:
            if not os.path.isfile(path):
                return {{"failed": True, "msg": f"Path '{{path}}' exists but is not a regular file."}}
            else:
                msg_parts.append(f"File '{{path}}' already exists.")
                
        if perm:
            octal_mode = int(str(perm), 8)
            current_mode = os.stat(path).st_mode & 0o777
            if current_mode != octal_mode:
                os.chmod(path, octal_mode)
                changed = True
                msg_parts.append("Permissions updated.")

        uid = -1
        gid = -1
        if user:
            try:
                uid = pwd.getpwnam(user).pw_uid
            except KeyError:
                return {{"failed": True, "msg": f"User '{{user}}' does not exist."}}
        if group:
            try:
                gid = grp.getgrnam(group).gr_gid
            except KeyError:
                return {{"failed": True, "msg": f"Group '{{group}}' does not exist."}}
                
        if uid != -1 or gid != -1:
            stat_info = os.stat(path)
            current_uid = stat_info.st_uid
            current_gid = stat_info.st_gid
            
            set_uid = uid if uid != -1 else current_uid
            set_gid = gid if gid != -1 else current_gid
            
            if current_uid != set_uid or current_gid != set_gid:
                os.chown(path, set_uid, set_gid)
                changed = True
                msg_parts.append("Ownership updated.")
                
        return {{"changed": changed, "msg": " ".join(msg_parts)}}
    except PermissionError:
        return {{"failed": True, "msg": f"Permission denied while trying to access '{{path}}'."}}
    except Exception as e:
        return {{"failed": True, "msg": f"An unexpected error occurred: {{str(e)}}"}}

result = _execute_remote_touch_logic(path={path!r}, perm={perm!r}, user={user!r}, group={group!r})
print(json.dumps(result))
"""
    
    # We format the script with the variables (safely quoting strings using !r)
    formatted_script = python_script_template.format(
        path=path,
        perm=perm,
        user=user,
        group=group
    )

    # Encode to base64 to avoid quoting/escaping issues over SSH
    encoded_script = base64.b64encode(formatted_script.encode('utf-8')).decode('utf-8')

    command = f"sudo -S python3 -c \"import base64, sys; exec(base64.b64decode(sys.argv[1]).decode('utf-8'))\" \"{encoded_script}\""
    
    return command