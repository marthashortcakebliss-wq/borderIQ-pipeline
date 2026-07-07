import re
import pandas as pd
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).parent.parent / "data"
GAZETTE_FILE = DATA_DIR / "eac_gazette_19_2025_excerpt.txt"

COUNTRY_MAP = {
    "Uganda": "UG", "Kenya": "KE", "Tanzania": "TZ",
    "Rwanda": "RW", "Burundi": "BI", "South Sudan": "SS", "DRC": "CD",
}

NEW_RATE_PATTERN = re.compile(r"apply\s+(?:a\s+|import\s+)?duty\s+rate\s+of\s+(\d+(?:\.\d+)?)\s*%")
OLD_RATE_PATTERN = re.compile(r"EAC CET rate of (\d+(?:\.\d+)?)\s*%")


def parse_gazette_line(line: str):
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) != 4:
        return None

    sn_hs, description, decision_text, country_codes_raw = parts
    hs_match = re.search(r"([\d.]{4,10})$", sn_hs)
    if not hs_match:
        return None
    hs_code = hs_match.group(1)

    new_rate_match = NEW_RATE_PATTERN.search(decision_text)
    if not new_rate_match:
        return None
    duty_rate = float(new_rate_match.group(1))

    old_rate_match = OLD_RATE_PATTERN.search(decision_text)
    old_rate = float(old_rate_match.group(1)) if old_rate_match else None

    country_codes = [c.strip() for c in country_codes_raw.split(",")]

    return {
        "hs_code": hs_code,
        "description": description,
        "decision_text": decision_text,
        "previous_cet_rate": old_rate,
        "duty_rate": duty_rate,
        "destination_countries": country_codes,
    }


def parse_gazette_file() -> pd.DataFrame:
    records = []
    with open(GAZETTE_FILE, "r") as f:
        for line in f:
            if "|" not in line:
                continue
            parsed = parse_gazette_line(line)
            if parsed is None:
                continue
            for country in parsed["destination_countries"]:
                records.append({
                    "hs_code": parsed["hs_code"],
                    "description": parsed["description"],
                    "category": "Gazette Stay of Application",
                    "origin_country": "XX",
                    "destination_country": country,
                    "duty_rate": parsed["duty_rate"],
                    "vat_rate": None,
                    "excise_rate": None,
                    "effective_date": date(2025, 6, 30),
                    "source": "EAC Gazette Vol. AT 1 No. 19, Legal Notice EAC/171/2025",
                })
    return pd.DataFrame(records)
