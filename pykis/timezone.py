
from datetime import date, datetime, timedelta, timezone


tz_kst = timezone(timedelta(hours=9))

def ensure_datetime(dt: datetime | date | None) -> datetime:
    if dt is None:
        return datetime.now(tz_kst)
    if isinstance(dt, date):
        return datetime.combine(dt, datetime.min.time(), tzinfo=tz_kst)
    return dt

def ensure_date(dt: date | None) -> date:
    if dt: return dt
    return date.today()
