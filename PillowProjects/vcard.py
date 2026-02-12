# vcard_export.py
from __future__ import annotations
import re

def _esc(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace(";", r"\;").replace(",", r"\,").replace("\n", r"\n")

def _digits_only(phone: str) -> str:
    return re.sub(r"[^\d+]", "", phone or "")

def write_vcard(
    path: str,
    full_name: str,
    company: str = "",
    phone: str = "",
    email: str = "",
    linkedin_url: str = "",
    website: str = "",
) -> None:
    fn = _esc(full_name.strip())
    org = _esc(company.strip())
    tel = _digits_only(phone.strip())
    eml = email.strip()
    li = linkedin_url.strip()
    web = website.strip()

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{fn}",
    ]
    if org:
        lines.append(f"ORG:{org}")
    if tel:
        lines.append(f"TEL;TYPE=CELL:{tel}")
    if eml:
        lines.append(f"EMAIL;TYPE=INTERNET:{_esc(eml)}")
    if web:
        lines.append(f"URL:{_esc(web)}")
    if li:
        lines.append(f"URL:{_esc(li)}")
    lines.append("END:VCARD")

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
