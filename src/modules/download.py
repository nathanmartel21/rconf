def run(params: dict) -> str:
    """Generates a bash script to safely and idempotently download files."""
    url = params.get('url')
    dest = params.get('dest')
    
    if not url or not dest:
        raise ValueError("The 'url' and 'dest' parameters are required for the download module.")

    force = params.get('force', False)
    insecure = params.get('insecure', False)
    username = params.get('username')
    password = params.get('password')
    timeout = params.get('timeout', 30)
    checksum = params.get('checksum')
    perm = params.get('perm')
    user = params.get('user')
    group = params.get('group')
    headers = params.get('headers', {})
    extract = params.get('extract', False)

    # Build curl options
    curl_opts = ["-sSL", "-f", f"--connect-timeout {int(timeout)}"]
    
    if insecure:
        curl_opts.append("-k")
        
    if username and password:
        user_escaped = username.replace("'", "'\\''")
        pass_escaped = password.replace("'", "'\\''")
        curl_opts.append(f"-u '{user_escaped}:{pass_escaped}'")
    elif username:
        user_escaped = username.replace("'", "'\\''")
        curl_opts.append(f"-u '{user_escaped}'")

    if isinstance(headers, dict):
        for k, v in headers.items():
            h_escaped = f"{k}: {v}".replace("'", "'\\''")
            curl_opts.append(f"-H '{h_escaped}'")

    curl_opts_str = " ".join(curl_opts)

    # handle checksums
    checksum_type = ""
    expected_checksum = ""
    checksum_cmd = ""
    
    if checksum:
        if ':' in checksum:
            checksum_type, expected_checksum = checksum.split(':', 1)
        else:
            checksum_type = "sha256"
            expected_checksum = checksum
        
        checksum_type = checksum_type.lower()
        if checksum_type == "md5":
            checksum_cmd = "md5sum"
        elif checksum_type == "sha1":
            checksum_cmd = "sha1sum"
        elif checksum_type == "sha256":
            checksum_cmd = "sha256sum"
        elif checksum_type == "sha512":
            checksum_cmd = "sha512sum"
        else:
            raise ValueError(f"Unsupported checksum type: {checksum_type}")

    dest_escaped = dest.replace("'", "'\\''")
    url_escaped = url.replace("'", "'\\''")
    
    script = f"""
DEST='{dest_escaped}'
TMP_DEST="${{DEST}}.tmp.$$"
DOWNLOAD=false

if [ -f "$DEST" ]; then
"""
    if force:
        script += "    DOWNLOAD=true\n"
    elif checksum_cmd:
        script += f"""
    if type {checksum_cmd} >/dev/null 2>&1; then
        ACTUAL=$({checksum_cmd} "$DEST" | awk '{{print $1}}')
        if [ "$ACTUAL" != "{expected_checksum}" ]; then
            DOWNLOAD=true
        fi
    else
        DOWNLOAD=true
    fi
"""
    else:
        script += "    DOWNLOAD=false\n"
        
    script += f"""
else
    DOWNLOAD=true
fi

if [ "$DOWNLOAD" = "true" ]; then
    curl {curl_opts_str} -o "$TMP_DEST" '{url_escaped}'
    CURL_RET=$?
    if [ $CURL_RET -ne 0 ]; then rm -f "$TMP_DEST"; echo "Download failed with curl exit code $CURL_RET" >&2; exit $CURL_RET; fi
"""
    if checksum_cmd:
        script += f"""
    ACTUAL=$({checksum_cmd} "$TMP_DEST" | awk '{{print $1}}')
    if [ "$ACTUAL" != "{expected_checksum}" ]; then rm -f "$TMP_DEST"; echo "Checksum mismatch! Expected {expected_checksum}, got $ACTUAL" >&2; exit 1; fi
"""
    script += f"""
    mv -f "$TMP_DEST" "$DEST"
    {'''if [[ "$DEST" == *.tar.gz ]] || [[ "$DEST" == *.tgz ]]; then tar -xzf "$DEST" -C "$(dirname "$DEST")"; elif [[ "$DEST" == *.tar.bz2 ]]; then tar -xjf "$DEST" -C "$(dirname "$DEST")"; elif [[ "$DEST" == *.tar ]]; then tar -xf "$DEST" -C "$(dirname "$DEST")"; elif [[ "$DEST" == *.zip ]]; then unzip -o "$DEST" -d "$(dirname "$DEST")"; fi''' if extract else ""}
fi
"""
    if perm: script += f"chmod '{perm}' \"$DEST\"\n"
    if user: script += f"chown '{user}' \"$DEST\"\n"
    if group: script += f"chgrp '{group}' \"$DEST\"\n"

    escaped_script = script.strip().replace("'", "'\\''")
    return f"sudo -S bash -c '{escaped_script}'"