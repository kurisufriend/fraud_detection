import pandas, seaborn
from requests import get
from sys import argv, exit
import sklearn
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection

# check args
if "help" in argv:
    print(f"""USAGE:\npython3 main.py""")
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

# isolate fraudulent & legitimate sets
fraud_set = data.loc[data["Class"] == 1]
legit_set = data.loc[data["Class"] == 0]

# get variables ready for training
x = data.loc[:, "V1":"V28"]
y = data["Class"]

xtrain, xtest, ytrain, ytest = sklearn.model_selection.train_test_split(x, y, random_state = 0)

# train
classifier = sklearn.linear_model.SGDClassifier()
classifier.fit(xtrain, ytrain)

# predict
predictions = classifier.predict(xtest)

# save
accuracy = sklearn.metrics.accuracy_score(ytest, predictions)
save = input(f"accuracy: {accuracy}, save data to .csv? [y/n]")
data["guess"] = classifier.predict(x).flatten()
print(data)
if save.lower() == "y":
    data.to_csv("guesses.csv")
else:
    print("exited without saving")