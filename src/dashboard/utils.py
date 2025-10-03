import re

def normalize_title(s: str) -> str:
    s = " ".join(s.strip().split())
    if not s:
        return s
    return s[0].upper() + s[1:]

def slugify(s: str) -> str:
    s = normalize_title(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")
