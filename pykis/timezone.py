
from datetime import datetime, timedelta, timezone


tz_kst = timezone(timedelta(hours=9))

def ensure_datetime(dt: datetime | None) -> datetime:
    if dt: return dt
    return datetime.now(tz_kst)
