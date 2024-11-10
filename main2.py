"""
This is just for checking of python learning
"""

from datetime import datetime, timedelta, timezone

indian_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
print(indian_time)


indian_time = datetime.now()
print(indian_time)

indian_time = datetime.now(timezone(timedelta(hours=0, minutes=30)))
print(indian_time)

