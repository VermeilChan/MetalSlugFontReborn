import math
import platform
from datetime import datetime
from uuid import uuid4


def readable_size(size_bytes):
    if size_bytes == 0:
        return "0 bytes"
    units = ["bytes", "KB", "MB"]
    power = int(math.log(size_bytes, 1024))
    power = min(power, len(units) - 1)
    size = size_bytes / (1024**power)
    return f"{size:.2f} {units[power]}"


def normalize_architecture(arch):
    mapping = {
        "x86_64": "64-Bit",
        "amd64": "AMD64",
        "arm64": "ARM64",
        "aarch64": "ARM64",
        "64bit": "64-Bit",
    }
    return mapping.get(arch.lower(), arch)


def get_windows_feature_update():
    if platform.system() != "Windows":
        return None

    try:
        import winreg

        key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            display_version, _ = winreg.QueryValueEx(key, "DisplayVersion")
            return display_version
    except Exception:
        return None


def get_system_info():
    system = platform.system()
    arch = normalize_architecture(platform.machine())
    if system == "Windows":
        edition = platform.win32_edition()
        release = platform.release()
        version = platform.version()
        feature_update = get_windows_feature_update()

        feature_part = f"{feature_update} " if feature_update else ""
        return f"{system} {release} {feature_part}{edition} (Build {version}) {arch}".strip()
    elif system == "Linux":
        try:
            os_release = platform.freedesktop_os_release()
            if "PRETTY_NAME" in os_release:
                return f"{os_release['PRETTY_NAME']} {arch}"
            name = os_release.get("NAME", "Linux")
            version = os_release.get("VERSION", "")
            if name or version:
                return f"{name} {version} {arch}".strip()
        except OSError:
            system_name = platform.system()
            release = platform.release()
            return f"{system_name} {release} {arch}"
    elif system == "Darwin":
        mac_version, *_ = platform.mac_ver()
        return f"macOS {mac_version or platform.release()} {arch}"


msfr_version = f"3.1.0 ({uuid4().hex[:7]})"
build_date = datetime.now().strftime("%Y-%m-%d (%A, %B %d)")

system_info = get_system_info()
