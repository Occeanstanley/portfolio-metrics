import os, csv, requests

USER = os.getenv("HF_USERNAME", "occeanstanley9")
BASE = f"https://huggingface.co/api/models?author={USER}"

def main():
    os.makedirs("data", exist_ok=True)
    try:
        r = requests.get(BASE, timeout=30)
        r.raise_for_status()
        models = r.json() or []
    except Exception:
        models = []
    with open("data/hf_models.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model_id","downloads","likes","private"])
        for m in models:
            w.writerow([m.get("modelId",""), m.get("downloads",0), m.get("likes",0), m.get("private",False)])

if __name__ == "__main__":
    main()
