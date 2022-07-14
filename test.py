import pandas
data = pandas.read_csv("creditcard.csv")
guessed_class = []
for r in data.iterrows():
    good = True
    if abs(r[1]["V17"] - -6.665836399449663) < abs(r[1]["V17"] - 0.01153506325212925):
        good = False
    guessed_class.append(0 if good else 1)
data["guess"] = guessed_class
print(data.head(10))
data.to_csv("woo2.csv")