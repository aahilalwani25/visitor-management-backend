import pandas as pd

def update_excel(name, cnic, checkin=True, timestamp=None):

    file = 'visitors.xlsx'
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    try:
        df = pd.read_excel(file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "CNIC", "Check-in", "Check-out"])

    row_index = df[df["CNIC"] == cnic].index

    if len(row_index) == 0:
        new_row = {"Name": name, "CNIC": cnic, "Check-in": timestamp_str if checkin else "", "Check-out": timestamp_str if not checkin else ""}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        idx = row_index[0]
        if checkin:
            if pd.isna(df.at[idx, "Check-in"]) or df.at[idx, "Check-in"] == "":
                df.at[idx, "Check-in"] = timestamp_str
            else:
                df.at[idx, "Check-in"] += f" | {timestamp_str}"
        else:
            if pd.isna(df.at[idx, "Check-out"]) or df.at[idx, "Check-out"] == "":
                df.at[idx, "Check-out"] = timestamp_str
            else:
                df.at[idx, "Check-out"] += f" | {timestamp_str}"

    df.to_excel(file, index=False)