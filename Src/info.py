from uuid import uuid4
from datetime import datetime

msfr_version = "1.10.1"
pyinstaller_version = "6.10.0"
pyside6_version = "6.7.3"
pillow_version = "10.4.0"

latest_commit_sha = uuid4().hex[:7]  # ik im autistic
msfr_version += f" ({latest_commit_sha})"

current_datetime = datetime.now()
formatted_date_time = current_datetime.strftime("%Y-%m-%d (%A, %B %d, %Y)")
build_date = formatted_date_time
