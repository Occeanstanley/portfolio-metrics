import os
import pandas as pd

os.makedirs("data", exist_ok=True)

def safe_read(path, **kwargs):
    if os.path.exists(path):
        return pd.read_csv(path, **kwargs)
    return pd.DataFrame()

repos = safe_read("data/github_repos.csv")
commits = safe_read("data/github_commits.csv")
langs = safe_read("data/github_languages.csv")

if not commits.empty:
    commits_summary = (commits.groupby("repo", as_index=False)["commits"]
                             .sum().rename(columns={"commits": "commits_180d"}))
else:
    commits_summary = pd.DataFrame(columns=["repo","commits_180d"])

if not repos.empty:
    summary = repos.merge(commits_summary, how="left", on="repo")
    summary["commits_180d"] = summary["commits_180d"].fillna(0).astype(int)
else:
    summary = pd.DataFrame(columns=["repo","stars","forks","language","updated_at","commits_180d"])

summary.to_csv("data/github_repo_summary.csv", index=False)
