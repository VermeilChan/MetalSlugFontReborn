import math
import platform
from uuid import uuid4
from datetime import datetime

def readable_size(size_bytes):
    if size_bytes == 0:
        return "0 bytes"
    units = ["bytes", "KB", "MB"]
    power = int(math.log(size_bytes, 1024))
    power = min(power, len(units) - 1)
    size = size_bytes / (1024 ** power)
    return f"{size:.2f} {units[power]}"

def normalize_architecture(arch):
    mapping = {
        "x86_64": "64-Bit",
        "AMD64": "64-Bit",
        "arm64": "ARM64",
        "aarch64": "ARM64",
        "64bit": "64-Bit",
    }
    return mapping.get(arch, arch)

def get_system_info():
    system = platform.system()
    arch = normalize_architecture(platform.architecture()[0])

    try:
        if system == "Windows":
            edition = platform.win32_edition()
            return f"{system} {edition} {arch}"

        elif system == "Linux":
            os_release = platform.freedesktop_os_release()
            name = os_release.get("PRETTY_NAME")
            if not name:
                name = f"{os_release.get('NAME', 'Linux')} {os_release.get('VERSION', '')}".strip()
            return f"{name} {arch}"

        elif system == "Darwin":
            return f"macOS {platform.release()} {normalize_architecture(platform.machine())}"

        else:
            return f"{system} {arch}"

    except Exception as error:
        return f"{system} (Error: {error})"

msfr_version = f"1.12.1 ({uuid4().hex[:7]})"
build_date = datetime.now().strftime("%Y-%m-%d (%A, %B %d, %Y)")

system_info = get_system_info()
