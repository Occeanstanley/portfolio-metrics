import os, requests, csv, datetime as dt, time
from collections import Counter

USERNAME = os.getenv("GITHUB_USERNAME", "occeanstanley9")
TOKEN = os.getenv("GH_TOKEN")  # set in GitHub Actions → repo secrets
BASE = "https://api.github.com"
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def paged_get(url, params=None):
    out, page = [], 1
    params = params or {}
    while True:
        q = params | {"per_page": 100, "page": page}
        r = requests.get(url, headers=HEADERS, params=q, timeout=30)
        if r.status_code == 202:
            time.sleep(2);  # stats endpoints sometimes return 202 (processing)
            continue
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        out += batch
        page += 1
    return out

def get_repos():
    return paged_get(f"{BASE}/users/{USERNAME}/repos", params={"type": "owner", "sort": "updated"})

def get_commit_activity(repo_full_name):
    # 52 weeks, daily counts list
    url = f"{BASE}/repos/{repo_full_name}/stats/commit_activity"
    for _ in range(5):  # retry for 202
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 202:
            time.sleep(2); continue
        if r.status_code != 200:
            return []
        weeks = r.json() or []
        rows = []
        for w in weeks:
            monday = dt.datetime.utcfromtimestamp(w["week"]).date()
            for i, c in enumerate(w["days"]):
                rows.append({"repo": repo_full_name, "date": (monday + dt.timedelta(days=i)).isoformat(), "commits": c})
        return rows
    return []

def main():
    os.makedirs("data", exist_ok=True)

    repos = get_repos()
    with open("data/github_repos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["repo","stars","forks","language","updated_at"])
        for r in repos:
            w.writerow([r["full_name"], r["stargazers_count"], r["forks_count"], r["language"], r["updated_at"]])

    all_commits = []
    for r in repos:
        all_commits += get_commit_activity(r["full_name"])
        time.sleep(0.2)

    cutoff = dt.date.today() - dt.timedelta(days=180)
    all_commits = [row for row in all_commits if dt.date.fromisoformat(row["date"]) >= cutoff]

    with open("data/github_commits.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["date","repo","commits"])
        for row in all_commits:
            w.writerow([row["date"], row["repo"], row["commits"]])

    lang_counts = Counter([r["language"] for r in repos if r.get("language")])
    with open("data/github_languages.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["language","repos"])
        for lang, c in lang_counts.items():
            w.writerow([lang, c])

if __name__ == "__main__":
    main()

