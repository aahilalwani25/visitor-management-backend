import re

def parse_cnic_text(raw_text: str) -> dict:
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    joined = "\n".join(lines)

    parsed_data = {
        "name": None,
        "cnic_number": None,
        "date_of_birth": None,
        "date_of_issue": None,
        "date_of_expiry": None,
        "country": None,
        "gender": None,
    }

    # Name – assume 2nd line after "National identity card"
    for idx, line in enumerate(lines):
        if "identity card" in line.lower() and idx + 1 < len(lines):
            parsed_data["name"] = lines[idx + 1]
            break

    # CNIC
    cnic_match = re.search(r"\d{5}-\d{7}-\d", joined)
    if cnic_match:
        parsed_data["cnic_number"] = cnic_match.group()

    # Dates
    dates = re.findall(r"\d{2}[./-]\d{2}[./-]\d{4}", joined)
    if len(dates) >= 3:
        parsed_data["date_of_birth"] = dates[0]
        parsed_data["date_of_issue"] = dates[1]
        parsed_data["date_of_expiry"] = dates[2]
    elif len(dates) == 2:
        parsed_data["date_of_birth"] = dates[0]
        parsed_data["date_of_issue"] = dates[1]

    # Country
    if "pakistan" in joined.lower():
        parsed_data["country"] = "Pakistan"

    # Gender
    if "male" in joined.lower():
        parsed_data["gender"] = "Male"
    elif "female" in joined.lower():
        parsed_data["gender"] = "Female"
    elif "m" in joined.lower():
        parsed_data["gender"] = "Male"

    return parsed_data
