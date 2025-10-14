import os, csv, datetime as dt
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

os.makedirs("data", exist_ok=True)
path = "data/github_commits.csv"
out = "data/forecast_commits_next30.csv"

if not os.path.exists(path):
    with open(out, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["metric","value","generated_at"])
        csv.writer(f).writerow(["forecast_commits_30d", 0, dt.datetime.utcnow().isoformat()+"Z"])
    raise SystemExit()

df = pd.read_csv(path, parse_dates=["date"])
daily = df.groupby("date", as_index=False)["commits"].sum()
if len(daily) < 7:
    forecast_sum = int(daily["commits"].sum())
else:
    daily["t"] = (daily["date"] - daily["date"].min()).dt.days
    X = daily[["t"]].values
    y = daily["commits"].values
    model = LinearRegression().fit(X, y)
    future_t = np.arange(daily["t"].max()+1, daily["t"].max()+31).reshape(-1,1)
    pred = model.predict(future_t)
    forecast_sum = max(0, int(np.sum(pred)))

with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["metric","value","generated_at"])
    w.writerow(["forecast_commits_30d", forecast_sum, dt.datetime.utcnow().isoformat()+"Z"])
