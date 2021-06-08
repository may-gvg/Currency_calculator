
import csv
from flask import Flask

app = Flask(__name__)

import requests

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")

data_from_json = response.json()
print(type(data_from_json))

csv_file = open("output.csv", 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file, delimiter=';')

rates = data_from_json[0]['rates']
for rate in rates:
    currency = rate['currency']
    code = rate['code']
    bid = rate['bid']
    ask = rate['ask']

    print(currency, code, bid, ask)
    writer.writerow([currency, code, bid, ask])

csv_file.close()
