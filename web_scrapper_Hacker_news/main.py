import requests
from flask import Flask, render_template, request, redirect#flask 덕분에 python으로 웹사이트를 만들기 쉬워진다.
base_url = "http://hn.algolia.com/api/v1"
# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"
# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"
# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

new_api = requests.get(new).json()
popular_api = requests.get(popular).json()

def check_db(value, db, api):
  fromDb = db.get(value)
  if fromDb:
    hits = fromDb
  else:
    hits = api["hits"]
    db[value] = hits
  return hits

@app.route("/")#누군가 /에 접속하면 function을 반환해준다 ===> 이게 홈페이지
def home():
  value = request.args.get('order_by')
  if value:
    value = value.lower()#?order_by의 value 받아오고 소문자화
    if value == "new":#받아온 value가 new일 때
      api = new_api
      hits = check_db(value, db, api)
    elif value == "popular":
      api = popular_api
      hits = check_db(value, db, api)
    else:
      return redirect("/")
  else:
    value = "popular"
    hits = check_db("popular", db, popular_api)
  title = value.capitalize()
  return render_template("index.html", order_by = value, hits=hits, title = title)

@app.route("/<id>")
def detail(id):
  api = requests.get(make_detail_url(id)).json()
  title = api['title']
  children = api['children']
  return render_template("detail.html", title = title, api=api, children = children)

app.run(host="0.0.0.0")#얘는 repl.it이기 때문에 넣어준 host 주소