from datetime import datetime, timedelta


def get_formatted_datetime(datetime: datetime = datetime.now(), pattern: str = "%Y-%m-%dT%H-%M-%S") -> str:
    return datetime.strftime(pattern)


def get_iso_datetime(datetime: datetime = datetime.now()) -> str:
    return datetime.isoformat()


def add_iso_datetime(datetime: datetime = datetime.now(),
                     hours: int = 0,
                     weeks: int = 0,
                     days: int = 0
                     ) -> str:
    delta = timedelta(
        weeks=weeks,
        days=days,
        hours=hours
    )
    return get_iso_datetime(datetime + delta)


def get_time_duration(start_datetime: datetime, end_datetime: datetime = datetime.now()) -> dict:
    delta = end_datetime - start_datetime
    return {
        'hours': delta.seconds // 3600,
        'minutes': (delta.seconds % 3600) // 60,
        'seconds': delta.seconds % 60
    }
