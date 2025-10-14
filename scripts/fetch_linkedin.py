import os, csv, requests

URL = os.getenv("LINKEDIN_CSV_URL")  # e.g., published Google Sheet CSV link

def main():
    os.makedirs("data", exist_ok=True)
    out = "data/linkedin_metrics.csv"
    if not URL:
        # keep existing file or seed minimal if missing
        if not os.path.exists(out):
            with open(out, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["date","followers","post_impressions_7d","profile_views_7d"])
                w.writerow(["2025-10-13","1472","2510","195"])
        return

    try:
        r = requests.get(URL, timeout=30)
        r.raise_for_status()
        with open(out, "wb") as f:
            f.write(r.content)
    except Exception:
        # leave previous file in place if fetch fails
        pass

if __name__ == "__main__":
    main()
