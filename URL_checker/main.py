import requests, os

def url_check():
  print("Welcome to IsItDown.py!\nPlease write a URL or URLs you want to check. (seperated by comma)")
  url_list = list(input().split(","))
  for i in url_list:
    i = i.strip().lower()
    try:
      j = i if (i.find('http://') == 0 or i.find('https://') == 0) else 'http://'+ i
      print(f'{j} is up!') if requests.get(j).status_code == 200 else print(f'{j} is down!')
    except:
      print(f'{i} is not a valid URL.')
  start_over()

def start_over():
  x= str(input("Do you want to start over?: y/n "))
  (os.system('clear'), url_check()) if x == 'y' else print("Ok. bye!") if x == 'n' else (print("That's not a valid answer."), start_over())
  
url_check()