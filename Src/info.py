from datetime import datetime
from subprocess import run, DEVNULL, PIPE, CalledProcessError

msfr_version = "1.9.3"
pyinstaller_version = "6.10.0"
pyside2_version = "5.15.2.1"
pillow_version = "10.4.0"
build_date = "N/A"
config_file = "config.ini"

current_datetime = datetime.now()
formatted_date_time = current_datetime.strftime("%Y-%m-%d (%A, %B %d, %Y)")
build_date = formatted_date_time

try:
    result = run(
        ["git", "rev-parse", "--short", "HEAD"],
        stdout=PIPE,
        stderr=DEVNULL,
        text=True,
        check=True,
    )
    latest_commit_sha = result.stdout.strip()
    msfr_version += f" ({latest_commit_sha})"
except (CalledProcessError, FileNotFoundError):
    msfr_version += " (N/A)"
