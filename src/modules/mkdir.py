import os
import sys
import json
import base64
import pwd
import grp

def _execute_remote_mkdir_logic(path, perm='0755', user=None, group=None):
    """
    Creates a directory if it doesn't exist and returns the task result.
    """
    if not path:
        return {"failed": True, "msg": "The 'path' parameter is required."}

    changed = False
    msg_parts = []

    try:
        # Convert string perm (like '0755') to an octal integer
        octal_mode = int(str(perm), 8)
        
        if not os.path.exists(path):
            os.makedirs(path, mode=octal_mode)
            changed = True
            msg_parts.append(f"Directory '{path}' was successfully created.")
        else:
            # Check if it's a directory
            if not os.path.isdir(path):
                return {"failed": True, "msg": f"Path '{path}' exists but is not a directory."}
            else:
                msg_parts.append(f"Directory '{path}' already exists.")

        uid = -1
        gid = -1

        if user:
            try:
                uid = pwd.getpwnam(user).pw_uid
            except KeyError:
                return {"failed": True, "msg": f"User '{user}' does not exist."}
                
        if group:
            try:
                gid = grp.getgrnam(group).gr_gid
            except KeyError:
                return {"failed": True, "msg": f"Group '{group}' does not exist."}

        if uid != -1 or gid != -1:
            stat_info = os.stat(path)
            current_uid = stat_info.st_uid
            current_gid = stat_info.st_gid
            
            if (uid != -1 and current_uid != uid) or (gid != -1 and current_gid != gid):
                os.chown(path, uid, gid)
                changed = True
                msg_parts.append("Ownership updated.")

        return {"changed": changed, "msg": " ".join(msg_parts)}

    except PermissionError:
        return {"failed": True, "msg": f"Permission denied while trying to access '{path}'."}
    except Exception as e:
        return {"failed": True, "msg": f"An unexpected error occurred: {str(e)}"}

def run(params: dict) -> str:
    """
    Generates a shell command string to execute the mkdir logic on the remote host.
    """
    path = params.get('path')
    perm = params.get('perm', '0755')
    user = params.get('user')
    group = params.get('group')

    python_script_template = """
import os, sys, json, pwd, grp

def _execute_remote_mkdir_logic(path, perm='0755', user=None, group=None):
    if not path:
        return {{"failed": True, "msg": "The 'path' parameter is required."}}
    changed = False
    msg_parts = []
    try:
        octal_mode = int(str(perm), 8)
        if not os.path.exists(path):
            os.makedirs(path, mode=octal_mode)
            changed = True
            msg_parts.append(f"Directory '{{path}}' was successfully created.")
        else:
            if not os.path.isdir(path):
                return {{"failed": True, "msg": f"Path '{{path}}' exists but is not a directory."}}
            else:
                msg_parts.append(f"Directory '{{path}}' already exists.")
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
            if (uid != -1 and current_uid != uid) or (gid != -1 and current_gid != gid):
                os.chown(path, uid, gid)
                changed = True
                msg_parts.append("Ownership updated.")
        return {{"changed": changed, "msg": " ".join(msg_parts)}}
    except PermissionError:
        return {{"failed": True, "msg": f"Permission denied while trying to access '{{path}}'."}}
    except Exception as e:
        return {{"failed": True, "msg": f"An unexpected error occurred: {{str(e)}}"}}

result = _execute_remote_mkdir_logic(path={path!r}, perm={perm!r}, user={user!r}, group={group!r})
print(json.dumps(result))
"""
    
    formatted_script = python_script_template.format(
        path=path,
        perm=perm,
        user=user,
        group=group
    )

    encoded_script = base64.b64encode(formatted_script.encode('utf-8')).decode('utf-8')

    command = f"sudo -S python3 -c \"import base64, sys; exec(base64.b64decode(sys.argv[1]).decode('utf-8'))\" \"{encoded_script}\""
    
    return command