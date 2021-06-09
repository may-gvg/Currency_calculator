
from flask import request, redirect
import requests
from flask import render_template
import csv
from flask import Flask

app = Flask(__name__)




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

@app.route ('/waluty', methods=['GET', 'POST'])
def waluty():
   if request.method == 'GET':
       print("We received GET")
       return render_template("waluty.html")
   elif request.method == 'POST':
       print("We received POST")
       print(request.form)
       currency = request.form.get('zczego')
       money = float(request.form.get('kwota'))
       USD = 3.70
       EUR = 4.51
       CHF = 4.13
       xstr = ""
       print("Kwota: " + str(money))
       print("currenty: " + currency)
       if currency == "USD":
           xstr = str(round(money / USD, 3))
       elif currency == "EUR":
           xstr = str(round(money / EUR, 3))
       elif currency == "CHF":
           xstr = str(round(money / CHF, 3))
       print("xstr: " + xstr)

       return render_template("waluty.html", wynik=xstr)



