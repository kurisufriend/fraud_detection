import pandas, seaborn
from requests import get
from sys import argv, exit

# chack args
cmds = ["and", "max"]
if len(argv) < 2 or argv[1] not in cmds:
    print(f"""USAGE:\npython3 main.py <{'|'.join(cmds)}>
max = guess fraudulent if the heuristic for the best column finds it
and = guess fraudulent if ALL the heuristics determined to be good find it""")
    exit(-1)

# download dataset if it isn't already present (too large for github)
try: open("creditcard.csv").read()
except FileNotFoundError:
    print("downloading dataset...")
    txt = get("https://the.silly.computer/creditcard.csv").text
    open("creditcard.csv", "w").write(txt)

# read dataset into dataframe
data = pandas.read_csv("creditcard.csv")
data['mean'] = data.mean(axis=1)

# isolate fraud & legitimate sets
fraud_set = data.loc[data["Class"] == 1]
legit_set = data.loc[data["Class"] == 0]

#find the best columns for determining fraud
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
    if (accuracy > .95) and col_name != "Class":
        print("good heuristic!")
        good_heuristics.append({"name": col_name, "fraud_mean": fm, "legit_mean": lm, "accuracy": accuracy})
    print("")
print(good_heuristics)

# create new dataframe with guesses based on found heuristics and chosen type (max = best column, and = all good columns must match)
guessed_class = []
best_heuristic = None
best_acc = 0
for h in good_heuristics:
    if h["accuracy"] > best_acc:
        best_acc = h["accuracy"]
        best_heuristic = h

print(f"using heuristic: {best_heuristic['name']}")
for r in data.iterrows():
    if argv[1] == "and":
        bools = []
        for h in good_heuristics:
            bools.append(abs(r[1][h["name"]] - h["fraud_mean"]) < abs(r[1][h["name"]] - h["legit_mean"]))
        fraud = all(bools)
        guessed_class.append(1 if fraud else 0)
    elif argv[1] == "max":
        good = True
        if abs(r[1][best_heuristic["name"]] - best_heuristic["fraud_mean"]) < abs(r[1][best_heuristic["name"]] - best_heuristic["legit_mean"]):
            good = False
        guessed_class.append(0 if good else 1)
data["guess"] = guessed_class
print(data.head(10))
data.to_csv("woo.csv")