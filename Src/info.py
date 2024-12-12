from uuid import uuid4
from datetime import datetime

msfr_version = "1.10.1"
pyinstaller_version = "6.11.1"
pyside6_version = "6.8.1"
pillow_version = "11.0.0"

latest_commit_sha = uuid4().hex[:7] # placeholder for sha
msfr_version += f" ({latest_commit_sha})"

current_datetime = datetime.now()
formatted_date_time = current_datetime.strftime("%Y-%m-%d (%A, %B %d, %Y)")
build_date = formatted_date_time
