from datetime import datetime, timezone


def utc_now_iso() -> str:
    """
    Return current UTC time as ISO-8601 string.
    """
    return datetime.now(timezone.utc).isoformat()


def iso_to_datetime(iso_str: str) -> datetime:
    """
    Convert ISO string to datetime object.
    """
    return datetime.fromisoformat(iso_str)
