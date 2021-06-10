import requests
import bs4
import pandas as pd
from datetime import datetime
import numpy as np
import xlrd

def req_wallet(wallet):

    now_time = datetime.now().strftime("%d-%m-%Y_%H:%M")
    url = f"https://www.blockchain.com/btc/address/{wallet}"
    print(url)
    result = requests.get(url)
    print(result)
    soup = bs4.BeautifulSoup(result.text, "lxml")
    btc = soup.find_all("div", class_="sc-8sty72-0 bFeqhe")
    usd = soup.find_all("div", class_="sc-10m3woc-0 sc-19bnflk-0 GYUxR izJzLI")

    data = []
    keys = []
    values = []
    usd_string = []

    for i in btc:
        span = i.find("span")
        data.append(span.string)

    for i in usd:
        span = i.find("span")
        usd_string.append(span.string)

    usd_print = usd_string[0].split()
    usd_values = [s for s in usd_print if any(xs in s for xs in "$")]

    keys.append(data[0])
    keys.append(data[4])
    keys.append(data[6])
    keys.append(data[8])
    keys.append(data[10])
    keys.append(data[6]+" USD")
    keys.append(data[8]+" USD")
    keys.append(data[10]+" USD")
    keys.append("Check Date")
    values.append([data[1]])
    values.append([data[5]])
    values.append([data[7]])
    values.append([data[9]])
    values.append([data[11]])
    values.append([usd_values[0].split("(")[1].split(")")[0]])
    values.append([usd_values[1].split("(")[1].split(")")[0]])
    values.append([usd_values[2].split("(")[1].split(")")[0]])
    values.append([now_time])
    line = dict(zip(keys, values))
    print(line)
    #
    # # df = pd.DataFrame(data=line)
    # #
    # # df.to_excel("Wallets.xlsx")





if __name__ == '__main__':

    wallet_list= []
    df = pd.read_excel(r"C:\Users\GZL_010\Desktop\wallets.xlsx")
    for col in df.columns:
        wallet_list.append(col)
        for val in df[col]:
            wallet_list.append(val)

    for wallet in wallet_list:
        try:
            req_wallet(wallet)
        except Exception as Error:
            print(f"Error happened on {wallet}")
            print(str(Error))
