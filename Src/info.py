from subprocess import check_output
from datetime import datetime

msfr_version = "1.9.2"
pyinstaller_version = "6.7.0"
pyside6_version = "6.7.1"
pillow_version = "10.3.0"
build_date = "2024-05-31 (Friday, May 31, 2024)"
config_file = "config.ini"

is_dev = False

if is_dev:
    current_datetime = datetime.now()
    formatted_date_time = current_datetime.strftime("%Y-%m-%d (%A, %B %d, %Y)")

    try:
        latest_commit_sha = check_output(
            ["git", "rev-list", "HEAD", "-1"], text=True
        ).strip()
        short_commit_sha = latest_commit_sha[:7]
        msfr_version += f" ({short_commit_sha})"
        build_date = formatted_date_time
    except Exception:
        msfr_version += "(N/A)"
        build_date = formatted_date_time
