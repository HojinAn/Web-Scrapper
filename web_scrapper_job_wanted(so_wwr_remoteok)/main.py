
"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import Flask, render_template, request, send_file, redirect
import os
import remoteok, wwr, so
from exporter import save_to_file

os.system("clear")

db={}
app = Flask("DayThirteen")

def whole_scrapper(term):
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
  post_list = []
  post_list.extend(so.scrapper(term, headers))
  post_list.extend(wwr.scrapper(term, headers))
  post_list.extend(remoteok.scrapper(term, headers))
  return post_list


@app.route("/")
def home():
  return render_template("home.html")


@app.route("/search")
def search():
  term = request.args.get('term')#term이 python이면
  term = term.lower()
  try:
    datas = db[term] #db['python']이 있으면 오류 발생하지 않는다
  except: #db['python']이 존재하지 않으면 윗줄에서 오류 발생하기 때문에 except 처리
    datas = whole_scrapper(term) #datas에 스크랩 정보 저장
    db[term] = datas #fakeDb에 저장하기
  return render_template("detail.html", datas = datas, term = term, number = len(datas))


@app.route("/export_to_csv")
def export():
  try:
    term = request.args.get('term')#term이 python? 이상한놈일수도
    if not term:
      raise Exception()
    
    term = term.lower()

    if not db[term]:#db로부터 받아온 자료가 없으면 exception 발생
      raise Exception()

    save_to_file(term, db[term])
    return send_file(f'{term}.csv', mimetype='application/x-csv', attachment_filename=f'{term}.csv', as_attachment=True)
#처음 csv는 send해줄 csv, mimetype = 'text/csv' : 파일 형식 
#as_attachment = True : Header 정보와 함께 보내기 위해 사용/ 이게 없으면 확장자를 못찾는다
#attachment_filename 은 저장하려는 이름과 send해줄 파일 이름이 다른 경우 이용
  except:
    return redirect("/")

app.run(host="0.0.0.0")
