from platform import system, architecture, win32_ver, win32_edition, freedesktop_os_release, mac_ver, machine

def readable_size(size_bytes):
    units = ["bytes", "KB", "MB"]
    size = size_bytes
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024

def normalize_architecture(arch):
    return {
        "x86_64": "64-Bit",
        "64bit": "64-Bit",
        "arm64": "ARM64",
        "aarch64": "ARM64",
    }.get(arch, arch)

def get_windows_info():
    try:
        version = win32_ver()[0]
        edition = win32_edition()
        arch = normalize_architecture(architecture()[0])
        return f"Windows {version} {edition} {arch}"
    except Exception as error:
        return f"Windows (Error: {error})"

def get_linux_info():
    try:
        distro = freedesktop_os_release()
        name = distro.get("NAME", "Linux")
        pretty_name = distro.get("PRETTY_NAME", "")
        version = distro.get("VERSION", "")
        version_id = distro.get("VERSION_ID", "")
        arch = normalize_architecture(architecture()[0])

        if pretty_name:
            return f"{pretty_name} {arch}"
        if version:
            return f"{version} {arch}"
        
        components = [name]
        if version_id:
            components.append(version_id)
        return f"{' '.join(components)} {arch}"

    except OSError:
        return f"Linux {normalize_architecture(architecture()[0])}"
    except Exception as error:
        return f"Linux (Error: {error})"

def get_macos_info():
    try:
        version = mac_ver()[0]
        arch = normalize_architecture(machine())
        return f"macOS {version} {arch}"
    except Exception as error:
        return f"macOS (Error: {error})"

def get_os_info():
    system_name = system()
    handlers = {
        "Windows": get_windows_info,
        "Linux": get_linux_info,
        "Darwin": get_macos_info,
    }
    handler = handlers.get(system_name)
    return handler() if handler else f"Unknown OS (System: {system_name})"

msfr_version = f"1.11.1 (49234ed)"
build_date = "2025-07-12 (Saturday, July 12, 2025)"
