from uuid import uuid4
from datetime import datetime

msfr_version = f"1.11.0 ({uuid4().hex[:7]})"
build_date = datetime.now().strftime("%Y-%m-%d (%A, %B %d, %Y)")