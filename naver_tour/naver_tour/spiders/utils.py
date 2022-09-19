from datetime import datetime, timedelta


def to_datetime(dt: str)-> datetime:
    return datetime.strptime(dt, '%Y%m%d')

def to_str(dt: datetime) -> str:
    return datetime.strftime(dt, '%Y%m%d')

def n_days(n: int):
    return timedelta(days=n)

def date_range(base: datetime, periods: int):
    for p in range(periods):
        yield base + n_days(p)

def date_iter(s: str, e: str):
    start_at = to_datetime(s)
    end_at = to_datetime(e)
    days = int((end_at- start_at).days)
    
    for s in date_range(start_at, periods=days):
        for e in date_range(s + n_days(1), periods=int((end_at-s).days)):
            yield to_str(s), to_str(e)
