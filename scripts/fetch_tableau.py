# Intentionally minimal: keeps tableau_views.csv if present, otherwise seeds it.
import os, csv, datetime as dt

SEED = [
    ("COVID-19 Trends in NYC", "77", "2025-10-13"),
    ("ElecMart 2018 Dashboard", "25", "2025-10-13"),
]

def main():
    os.makedirs("data", exist_ok=True)
    path = "data/tableau_views.csv"
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["viz_title","views","date"])
            for row in SEED: w.writerow(row)
    else:
        # no-op; you can edit this file monthly to append a new snapshot row
        pass

if __name__ == "__main__":
    main()
