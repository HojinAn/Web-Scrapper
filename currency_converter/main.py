import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

iban_url = "https://www.iban.com/currency-codes"
iban_result = requests.get(iban_url)
iban_soup = BeautifulSoup(iban_result.text, "html.parser")

trs = iban_soup.find("tbody").find_all("tr")
country_info=[]
n=0
print("Welcome to CurrencyConvert PRO 2000\n")

for i in range(len(trs)):
  country_name = trs[i].select_one("td:nth-child(1)").text
  country_code = trs[i].select_one("td:nth-child(3)").text
  if country_code == '':
    continue
  else:
    array_temp = []
    array_temp.append(country_name.capitalize())
    array_temp.append(country_code)
    country_info.append(array_temp)
    print(f"# {n} {country_info[n][0]}")
    n+=1

print("\nWhere are you from? Choose a country by number.")

def country_data():
  data = {}
  try:
    your_choose = int(input("\n#: "))
    if your_choose in range(n):
      print(f"{country_info[your_choose][0]}")
      data = {"name": f"{country_info[your_choose][0]}", "code": f"{country_info[your_choose][1]}"}
      return data
    else:
      print("Choose a number from the list")
      return country_data()
  except:
    print("That wasn't a number.")
    return country_data()
  
def convert_currency(fro,con):
  a=fro['code']
  b=con['code']
  print(f"\nHow many {a} do you want to convert to {b}?")
  amount = 0
  try:
    amount = int(input())
    amount_same = format_currency(amount, f"{a}", locale="ko_KR")
    if a == b:
      print(f"{amount_same} is {amount_same}")
    else:
      convert_url = f"https://wise.com/gb/currency-converter/{a}-to-{b}-rate?amount={amount}"
      convert_result = requests.get(convert_url)
      convert_soup = BeautifulSoup(convert_result.text, "html.parser")
      exchange_rate = float(convert_soup.find("div", {"class": "js-Calculator cc__header cc__header-spacing card card--with-shadow m-b-5"}).find("input", {"id":"rate"})["value"])
      exchange = int(amount * exchange_rate)
      converted_amount = format_currency(exchange, f"{b}", locale="ko_KR")
      print(f"{amount_same} is {converted_amount}")
  except:
    print("That wasn't a number.")
    return convert_currency(fro,con)

from_country = country_data()
print("\nNow choose another country.")
converted_to = country_data()
convert_currency(from_country,converted_to)