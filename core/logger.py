import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def log_to_existing_journal(rows, mode="Virtual"):
    """
    Logs screened trades to your Google Sheet in the 'DATA' sheet.
    Mode: Virtual | Live | Backtest
    """
    if not rows:
        print("[SKIP] No rows to log.")
        return

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1LDa-sS6MNKHJ0EpWntmso33nMKmRoCZ1AeLA1kIAqx4").worksheet("DATA")

    for i, row in enumerate(rows, start=1):
        if not all(key in row for key in ("Symbol", "Close", "Signal"))or not row.get("executed"):
            print(f"[WARN] Row {i} missing required fields or was not executed, skipped.")
            continue

        # BUILD


        data = [
                f"T{int(datetime.now().timestamp())}",            # Trade ID
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),      # Date
                row["Symbol"],                                     # STOCK
                "BUY",                                             # BUY/SELL
                "No",                                              # Trade Executed
                round(row["Close"], 2),                            # Entry Price
                "",                                                # Position Size (manual later)
                "", "", "", "", "", "",                            # Exit, SL, TP, R, PnL, Charges
                "",                                                # Net Profit
                "",                                                # W/L
                row["Signal"],                                     # STRATEGY
                f"{mode} - Auto",                                  # NOTES
                "No",                                              # Current Position
                ""                                                 # Capital
                ]



    sheet.append_row(data)

    print(f"[LOGGED] Entry added to journal: {row['Symbol']} - {row['Signal']}")

