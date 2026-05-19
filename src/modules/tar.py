def run(params: dict) -> str:
    """Generates a bash command to compress or extract tar archives on the remote host.

    Parameters
    ----------
    action : str, optional
        Either ``compress`` or ``extract``. Defaults to ``extract``.

    --- Extract mode (action: extract) ---

    src : str
        Path to the source archive file on the remote host. Required.
    dest : str, optional
        Destination directory where the archive should be extracted. If omitted,
        the directory containing ``src`` is used.
    strip : int, optional
        Number of leading path components to strip during extraction
        (passed as ``--strip-components``).
    perm : str, optional
        Permissions to set on the extracted tree (``chmod -R``). Applied after extraction.
    user : str, optional
        Owner to set on the extracted tree (``chown -R``). Applied after extraction.
    group : str, optional
        Group to set on the extracted tree (``chgrp -R``). Applied after extraction.
    force : bool, optional
        If ``true``, the destination directory is removed *before* extraction.
    overwrite : bool, optional
        If ``true``, existing files in the destination are overwritten without
        clearing the entire directory first. Defaults to ``false``.
    keep_newer : bool, optional
        If ``true``, do not overwrite existing files that are newer than the archive
        contents (``--keep-newer-files``). Defaults to ``false``.
    exclude : str or list, optional
        Pattern(s) to exclude from extraction (``--exclude``). Can be a single
        string or a list of strings.
    format : str, optional
        Explicit archive format. Auto-detected from extension if omitted.
        Supported: ``tar``, ``gz``, ``bz2``, ``xz``, ``zst``.

    --- Compress mode (action: compress) ---

    src : str
        Path to the file or directory to compress. Required.
    dest : str
        Destination archive path (e.g., ``/tmp/backup.tar.gz``). Required.
    format : str, optional
        Compression format. Auto-detected from the ``dest`` extension if omitted.
        Supported: ``tar``, ``gz``, ``bz2``, ``xz``, ``zst``.
    exclude : str or list, optional
        Pattern(s) to exclude from the archive (``--exclude``).
    transform : str, optional
        Sed transformation expression (``--transform``) applied to file names
        in the archive (e.g., ``s|^/opt/app|app|``).
    dereference : bool, optional
        Follow symlinks and archive the files they point to. Defaults to ``false``.
    """
    action = params.get('action', 'extract')

    if action == 'compress':
        return _compress(params)
    elif action == 'extract':
        return _extract(params)
    else:
        raise ValueError(f"Unknown action '{action}' for tar module. Use 'compress' or 'extract'.")


# ---------------------------------------------------------------------------
# Helper: escape a string for embedding in a single-quoted bash literal
# ---------------------------------------------------------------------------
def _sh_quote(s: str) -> str:
    return s.replace("'", "'\\''")


# ---------------------------------------------------------------------------
# Helper: build a case statement that auto-detects archive format
# ---------------------------------------------------------------------------
_EXTRACT_CASE = """\
case "$SRC" in
  *.tar.gz|*.tgz)          tar -xzf "$SRC" -C "$DEST" ;;
  *.tar.bz2|*.tbz2)        tar -xjf "$SRC" -C "$DEST" ;;
  *.tar.xz|*.txz)          tar -xJf "$SRC" -C "$DEST" ;;
  *.tar.zst)               tar --zstd -xf "$SRC" -C "$DEST" ;;
  *.tar)                   tar -xf "$SRC" -C "$DEST" ;;
  *.zip)                   unzip -o "$SRC" -d "$DEST" ;;
  *)                       tar -xf "$SRC" -C "$DEST" ;;
esac"""

_COMPRESS_CASE = """\
case "$DEST" in
  *.tar.gz|*.tgz)          tar -zcf "$DEST" -C "$(dirname "$SRC")" "$(basename "$SRC")" ;;
  *.tar.bz2|*.tbz2)        tar -jcf "$DEST" -C "$(dirname "$SRC")" "$(basename "$SRC")" ;;
  *.tar.xz|*.txz)          tar -Jcf "$DEST" -C "$(dirname "$SRC")" "$(basename "$SRC")" ;;
  *.tar.zst)               tar --zstd -cf "$DEST" -C "$(dirname "$SRC")" "$(basename "$SRC")" ;;
  *.tar)                   tar -cf "$DEST" -C "$(dirname "$SRC")" "$(basename "$SRC")" ;;
  *.zip)                   cd "$(dirname "$SRC")" && zip -r "$DEST" "$(basename "$SRC")" ;;
  *)                       tar -cf "$DEST" -C "$(dirname "$SRC")" "$(basename "$SRC")" ;;
esac"""


# ---------------------------------------------------------------------------
# Helper: map format name to tar option flag(s)
# ---------------------------------------------------------------------------
def _format_to_tar_flag(fmt: str) -> str:
    mapping = {
        'gz': 'z',
        'bz2': 'j',
        'xz': 'J',
        'zst': '--zstd',
        'tar': '',
    }
    f = fmt.lower()
    if f not in mapping:
        raise ValueError(
            f"Unsupported format '{fmt}'. Supported: gz, bz2, xz, zst, tar"
        )
    return mapping[f]


# ---------------------------------------------------------------------------
# Extract
# ---------------------------------------------------------------------------
def _extract(params: dict) -> str:
    src = params.get('src')
    if not src:
        raise ValueError("The 'src' parameter is required for the tar module (extract mode).")

    dest = params.get('dest')
    strip = params.get('strip', 0)
    perm = params.get('perm')
    user = params.get('user')
    group = params.get('group')
    force = params.get('force', False)
    overwrite = params.get('overwrite', False)
    keep_newer = params.get('keep_newer', False)
    exclude = params.get('exclude')
    fmt = params.get('format')

    src_q = _sh_quote(src)
    dest_q = _sh_quote(dest) if dest else ""

    # ── preamble ──────────────────────────────────────────────────────
    lines = [f"SRC='{src_q}'"]
    if dest:
        lines.append(f"DEST='{dest_q}'")
    else:
        lines.append('DEST="$(dirname "$SRC")"')

    if force:
        lines.append('rm -rf "$DEST"')
    lines.append('mkdir -p "$DEST"')

    # ── decide whether to use explicit flags or auto-detect ──────────
    use_auto_detect = fmt is None or fmt.lower() not in ('tar', 'gz', 'bz2', 'xz', 'zst')

    if use_auto_detect:
        lines.append(_EXTRACT_CASE)
    else:
        # Explicit format
        flag = _format_to_tar_flag(fmt)
        tar_opts = f"-x{flag}f" if flag else "-xf"

        extra = ""
        if isinstance(strip, int) and strip > 0:
            extra += f" --strip-components={strip}"
        if overwrite:
            extra += " --overwrite"
        if keep_newer:
            extra += " --keep-newer-files"
        if exclude:
            patterns = exclude if isinstance(exclude, list) else [exclude]
            for p in patterns:
                p_q = _sh_quote(p)
                extra += f" --exclude='{p_q}'"

        lines.append(f"tar {tar_opts} \"$SRC\" -C \"$DEST\"{extra}")

    # ── post-extraction permissions / ownership ──────────────────────
    post = []
    if perm:
        post.append(f"chmod -R '{_sh_quote(perm)}' \"$DEST\"")
    if user:
        post.append(f"chown -R '{_sh_quote(user)}' \"$DEST\"")
    if group:
        post.append(f"chgrp -R '{_sh_quote(group)}' \"$DEST\"")

    cmd = " && ".join(lines)
    if post:
        cmd += " && " + " && ".join(post)

    return f"sudo -S bash -c '{_sh_quote(cmd)}'"


# ---------------------------------------------------------------------------
# Compress
# ---------------------------------------------------------------------------
def _compress(params: dict) -> str:
    src = params.get('src')
    dest = params.get('dest')

    if not src or not dest:
        raise ValueError("The 'src' and 'dest' parameters are required for the tar module (compress mode).")

    fmt = params.get('format')
    exclude = params.get('exclude')
    transform = params.get('transform')
    dereference = params.get('dereference', False)

    src_q = _sh_quote(src)
    dest_q = _sh_quote(dest)

    lines = [f"SRC='{src_q}'", f"DEST='{dest_q}'"]
    lines.append('mkdir -p "$(dirname "$DEST")"')

    use_auto_detect = fmt is None or fmt.lower() not in ('tar', 'gz', 'bz2', 'xz', 'zst')

    if use_auto_detect:
        lines.append(_COMPRESS_CASE)
    else:
        flag = _format_to_tar_flag(fmt)
        tar_opts = f"-c{flag}f" if flag else "-cf"

        extra = ""
        if dereference:
            extra += " -h"
        if exclude:
            patterns = exclude if isinstance(exclude, list) else [exclude]
            for p in patterns:
                p_q = _sh_quote(p)
                extra += f" --exclude='{p_q}'"
        if transform:
            t_q = _sh_quote(transform)
            extra += f" --transform='{t_q}'"

        lines.append(
            f"tar {tar_opts} \"$DEST\"{extra} "
            f"-C \"$(dirname \"$SRC\")\" \"$(basename \"$SRC\")\""
        )

    cmd = " && ".join(lines)
    return f"sudo -S bash -c '{_sh_quote(cmd)}'"