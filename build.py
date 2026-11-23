"""Generate synthetic subscription data and build the dashboard (index.html).

All numbers are randomly generated sample data. No real company data is used.
Run:  python build.py
"""
import json, random, datetime as dt

random.seed(42)
TODAY = dt.date(2026, 11, 23)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]

# ---- 1. Monthly revenue by brand, 2026 (Nov = Nov 1-23) and prior-year comparison
rev = {
    "Brand A":  [12100, 13400, 14900, 15600, 16800, 17200, 16300, 15200, 15900, 16700, 10900],
    "Brand B":  [11800, 11200, 10500, 10100, 9700, 9200, 8800, 8500, 8200, 7900, 5400],
    "Partners": [2600, 2400, 2500, 2300, 2200, 2100, 2000, 2100, 2000, 1900, 1300],
}
prior_ytd = {"Brand A": 128000, "Brand B": 138000, "Partners": 30100}
prior_mtd = {"Brand A": 8700, "Brand B": 7600, "Partners": 1500}

# ---- 2. Synthetic active subscriptions
PLANS = {
    "Annual":    dict(w=0.60, prices=[149, 179, 199, 249]),
    "Monthly":   dict(w=0.33, prices=[19.99, 24.99, 29.99]),
    "Weekly":    dict(w=0.05, prices=[9.99, 12.99, 14.99]),
    "Quarterly": dict(w=0.02, prices=[59.99]),
}
BRANDS = [("Brand A", 0.52), ("Brand B", 0.40), ("Partners", 0.08)]
SEASON = {12: 1.4, 1: 2.2, 2: 1.5, 3: 1.0, 4: .9, 5: .8, 6: .7, 7: .6, 8: .8, 9: 1.0, 10: 1.0, 11: .9}
days = [TODAY - dt.timedelta(days=i) for i in range(364, -1, -1)]
day_w = [SEASON[d.month] for d in days]
PERIOD = {"Weekly": 7, "Monthly": 30, "Quarterly": 91}
subs = []
for _ in range(1460):
    plan = random.choices(list(PLANS), [p["w"] for p in PLANS.values()])[0]
    brand = random.choices([b for b, _ in BRANDS], [w for _, w in BRANDS])[0]
    price = random.choice(PLANS[plan]["prices"])
    if plan == "Annual":
        signup = random.choices(days, day_w)[0]
        try:
            nxt = signup.replace(year=signup.year + 1)
        except ValueError:
            nxt = signup + dt.timedelta(days=365)
    else:
        nxt = TODAY + dt.timedelta(days=random.randint(1, PERIOD[plan]))
    subs.append([plan, brand, price, nxt.isoformat()])

# ---- 3. Acquisition funnel by source
sources = []
for i in range(1, 11):
    inst = random.randint(1800, 7400)
    reg = random.uniform(0.45, 0.93)
    kyc = random.uniform(0.10, 0.24)
    ftd = random.uniform(0.45, 0.65)
    ent = random.uniform(0.68, 0.84)
    act = random.uniform(0.03, 0.15)
    r = round(inst * reg); k = round(r * kyc); f = round(k * ftd); e = round(f * ent); a = round(inst * act)
    sources.append(dict(name=f"Source {i}", installs=inst, reg=r, kyc=k, ftd=f, entry=e, active=a))

data = dict(
    asof=TODAY.isoformat(), months=MONTHS, revenue=rev, priorYtd=prior_ytd, priorMtd=prior_mtd,
    newShare=0.284, newSubs=1206, free=388, promoters=912,
    subs=subs, sources=sources,
)
json.dump(data, open("data/sample_data.json", "w"), separators=(",", ":"))
tpl = open("template.html").read()
open("index.html", "w").write(tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":"))))
print("subs:", len(subs), "| sources:", len(sources), "| index.html written")
