import requests
import bs4
import pandas as pd
from datetime import datetime
import time
import numpy as np
from openpyxl import load_workbook

def req_wallet(wallet):

    now_time = datetime.now().strftime("%d-%m-%Y_%H:%M")
    url = f"https://www.blockchain.com/btc/address/{wallet}"
    # print(url)
    result = requests.get(url)
    # print(result)


    def data_gathering(link):
        soup = bs4.BeautifulSoup(link.text, "lxml")
        btc = soup.find_all("div", class_="sc-8sty72-0 bFeqhe")
        usd = soup.find_all("div", class_="sc-10m3woc-0 sc-19bnflk-0 GYUxR izJzLI")
        last_transaction = soup.find_all("div", class_="kad8ah-0 fjudWa")


        data = []
        keys = []
        values = []
        usd_string = []
        last_transaction_string = []


        for i in btc:
            span = i.find("span")
            data.append(span.string)

        for i in usd:
            span = i.find("span")
            usd_string.append(span.string)

        for i in last_transaction:
            span = i.find("span")
            last_transaction_string.append(span.string)


        try:
            usd_print = usd_string[0].split()
            usd_values = [s for s in usd_print if any(xs in s for xs in "$")]
        except Exception as error_usd_string:
            print("Error happened during USD information collection - " + str(error_usd_string))

        try:
            keys.append(data[0])
            keys.append(data[4])
            keys.append(data[6])
            keys.append(data[8])
            keys.append(data[10])
            keys.append(data[6] + " USD")
            keys.append(data[8] + " USD")
            keys.append(data[10] + " USD")
            keys.append("Last Transaction Date")
            keys.append("Check Date")
            values.append(data[1])
            values.append(data[5])
            values.append(data[7])
            values.append(data[9])
            values.append(data[11])
            values.append(usd_values[0].split("(")[1].split(")")[0])
            values.append(usd_values[1].split("(")[1].split(")")[0])
            values.append(usd_values[2].split("(")[1].split(")")[0])
            values.append(last_transaction_string[0])
            values.append([now_time])
            line = dict(zip(keys, values))
            return line
        except Exception as error_line:
            print("Error occured while creating line - " + str(error_line))

    data = data_gathering(result)

    def write_to_excel(line):

        # new dataframe with same columns
        df = pd.DataFrame(data=line)
        writer = pd.ExcelWriter(r"Wallets.xlsx", engine='openpyxl')
        # write out the new sheet
        df.to_excel(writer, index=False, header=False)
        writer.save()
        writer.close()

        print(line)

    if result.status_code == 200:
        try:
            time.sleep(1)
            data_gathering(result)
        except Exception as Error:
            print("Response is not right -Trying again in 5 seconds " + str(Error))

        try:
            write_to_excel(data)

        except Exception as Error:
            print("Writing to Excel Failed " + str(Error))




    else:
        try:
            time.sleep(5)
            data_gathering(result)
        except Exception as Error:
            print("Error with data gathering " + str(Error))

        try:
            write_to_excel(data)
        except Exception as Error:
            print("Writing to Excel Failed " + str(Error))



if __name__ == '__main__':
    wallet_list = []
    df = pd.read_excel(r"C:\Users\GZL_010\Desktop\wallets.xlsx")

    for col in df.columns:
        wallet_list.append(col)
        for val in df[col]:
            wallet_list.append(val)
    print(wallet_list)

    for wallet in wallet_list:
        try:
            req_wallet(wallet)
        except Exception as Error:
            print(f"Error happened on {wallet}")
            try:
                print("Retrying - in 5 seconds")
                time.sleep(5)
                req_wallet(wallet)
            except Exception as Error:
                print("Retry Failed " + str(Error))

            print("Couldn't complete due to " + str(Error))
