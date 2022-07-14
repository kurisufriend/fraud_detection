import pandas, seaborn
from requests import get

try: open("creditcard.csv").read()
except FileNotFoundError:
    print("downloading dataset...")
    txt = get("https://the.silly.computer/creditcard.csv").text
    open("creditcard.csv", "w").write(txt)
