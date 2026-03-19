import re
from datetime import datetime


def extract_jd_experience(text: str) -> int:
    text = text.lower()
    text = text.replace("–", "-").replace("—", "-")

    range_match = re.search(r'(\d+)\s*(?:-|to)\s*(\d+)\s*(year|years|yr|yrs)', text)
    if range_match:
        return int(range_match.group(1))

    simple_match = re.search(r'(\d+(?:\.\d+)?)\+?\s*(year|years|yr|yrs)', text)
    if simple_match:
        return int(float(simple_match.group(1)))

    return 0


def parse_month_year(date_str: str):
    date_str = date_str.strip().title()
    for fmt in ("%b %Y", "%B %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def extract_resume_experience(text: str) -> int:
    text = text.lower()
    text = text.replace("–", "-").replace("—", "-")

    pattern = re.findall(
        r'('
        r'jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|'
        r'jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t)?(?:ember)?|'
        r'oct(?:ober)?|nov(?:ember)?|dec(?:ember)?'
        r')\s+(\d{4})\s*-\s*('
        r'present|current|'
        r'jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|'
        r'jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t)?(?:ember)?|'
        r'oct(?:ober)?|nov(?:ember)?|dec(?:ember)?'
        r')?\s*(\d{4})?',
        text,
        flags=re.IGNORECASE
    )

    total_months = 0

    for start_month, start_year, end_month, end_year in pattern:
        start_dt = parse_month_year(f"{start_month} {start_year}")
        if not start_dt:
            continue

        if end_month.lower() in ["present", "current"]:
            end_dt = datetime.now()
        elif end_month and end_year:
            end_dt = parse_month_year(f"{end_month} {end_year}")
            if not end_dt:
                continue
        else:
            continue

        months = (end_dt.year - start_dt.year) * 12 + (end_dt.month - start_dt.month)
        if months > 0:
            total_months += months

    if total_months == 0:
        matches = re.findall(r'(\d+(?:\.\d+)?)\+?\s*(year|years|yr|yrs)', text)
        if matches:
            return int(max(float(m[0]) for m in matches))

    return int(total_months / 12)