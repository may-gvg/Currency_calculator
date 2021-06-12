
from flask import request
from flask import render_template
import csv
from flask import Flask
import requests

app = Flask(__name__)

def read_csv():
    arr = {}
    csvfile = open('output.csv', newline='', encoding="UTF-8")
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        arr[row[1]] = row[3]
    return arr


try:
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data_from_json = response.json()
    print(type(data_from_json))
    csv_file = open("output.csv", 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file, delimiter=';')
except:
    print("Błąd")
    exit(1)


rates = data_from_json[0]['rates']
for rate in rates:
    currency = rate['currency']
    code = rate['code']
    bid = rate['bid']
    ask = rate['ask']

    print(currency, code, bid, ask)
    writer.writerow([currency, code, bid, ask])

csv_file.close()

@app.route ('/waluty', methods=['GET', 'POST'])
def waluty():
   waluty = read_csv()
   options = ""
   for waluta in waluty:
        options += '<option value="' + waluta + '">' + waluta + '</option>'
   print(options)


   if request.method == 'GET':
       print("We received GET")
       return render_template("waluty.html", options=options)
   elif request.method == 'POST':
       print("We received POST")
       print(request.form)
       currency = request.form.get('zczego')
       money = float(request.form.get('kwota'))
       waluty = read_csv()
       for waluta in waluty:
           if waluta == currency:
               wartosc = float(waluty[waluta])
       print("Wartosc: " + str(wartosc))
       przelicz = ""
       print("Kwota: " + str(money))
       print("currenty: " + currency)
       przelicz = str(round(money * wartosc, 3))
       print("przelicz: " + przelicz)

       return render_template("waluty.html", wynik=przelicz, options=options)


