import pandas, seaborn
from requests import get

try: open("creditcard.csv").read()
except FileNotFoundError:
    print("downloading dataset...")
    txt = get("https://the.silly.computer/creditcard.csv").text
    open("creditcard.csv", "w").write(txt)

data = pandas.read_csv("creditcard.csv")
data['mean'] = data.mean(axis=1)

fraud_set = data.loc[data["Class"] == 1]
legit_set = data.loc[data["Class"] == 0]

good_heuristics = []

for col_name in fraud_set.columns:
    fm = fraud_set[col_name].mean()
    lm = legit_set[col_name].mean()
    corr = 0
    incorr = 0
    for r in data.iterrows():
        if abs(r[1][col_name] - fm) < abs(r[1][col_name] - lm):
            if r[1]["Class"] == 1: corr += 1
            else: incorr += 1
        elif abs(r[1][col_name] - fm) > abs(r[1][col_name] - lm):
            if r[1]["Class"] == 0: corr += 1
            else: incorr += 1
            
    print(col_name)
    print(fm)
    print(lm)
    accuracy = corr/(corr+incorr)
    print(accuracy)
    if (accuracy > .98) and col_name != "Class":
        print("good heuristic!")
        good_heuristics.append({"name": col_name, "fraud_mean": fm, "legit_mean": lm})
    print("")

print(good_heuristics)

guessed_class = []
for r in data.iterrows():
    good = True
    for h in good_heuristics:
        if abs(r[1][h["name"]] - h["fraud_mean"]) < abs(r[1][h["name"]] - h["legit_mean"]):
            good = False
    guessed_class.append(0 if good else 1)
data["guess"] = guessed_class
print(data.head(10))
data.to_csv("woo.csv")