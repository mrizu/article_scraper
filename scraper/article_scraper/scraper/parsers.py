from datetime import datetime
import pytz


def normalize_iso_date(date_str: str, tz_name: str = "Europe/Warsaw") -> str:
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    warsaw_tz = pytz.timezone(tz_name)
    dt_local = dt.astimezone(warsaw_tz)

    return dt_local


def extract_domain(url):
    from urllib.parse import urlparse

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain
