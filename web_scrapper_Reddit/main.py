from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""


subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

app = Flask("DayEleven")

def get_html(subreddit):
  url = f"https://www.reddit.com/r/{subreddit}/top/?t=month"
  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, "html.parser")
  return soup

def check_upvotes(data):
  upvotes = data.find("div", {"style":"width:40px;border-left:4px solid transparent"}).text
  if 'k' in upvotes:
    upvotes = int(1000*float(upvotes.replace('k', '')))
  else:
    upvotes = int(upvotes)
  return upvotes

def get_data(subreddit, soup):
  data_list = []
  datas = soup.find_all("div", {"data-testid": "post-container"})
  for data in datas:
    background = data.find("div", {"data-click-id":"background"})
    span = background.find("span").text#span 내부 첫 text 받아오기
    if span == "promoted":
      continue#span 내부 text가 promoted이면 skip하기
    else:#promoted가 아니면 목록에 넣기
      try:
        data_dict = {}
        a = data.find('a', attrs = {"data-click-id": "timestamp"})
        data_dict['link'] = a.attrs['href']
        data_dict['upvotes'] = check_upvotes(data)
        data_dict['title'] = data.find("h3").text
        data_dict['subreddit'] = subreddit
        data_list.append(data_dict)
      except:#data object가 none인 경우 text 찾아주면 error 발생하기 때문에 error 처리
        continue
  return data_list

@app.route("/")
def home():
  return render_template("home.html", subreddits = subreddits)


@app.route("/read")
def read():
  data_list =[]
  list_to_return = []
  for i in range(len(subreddits)):
    subreddit = request.args.get(f'{subreddits[i]}')#on or None 출력
    if subreddit == "on":
      list_to_return.append(subreddits[i])#on인 subreddit 리스트에 추가
      soup = get_html(f'{subreddits[i]}')
      data_list.extend(get_data(f'{subreddits[i]}', soup))
    else:
      continue
  data_list = reversed(sorted(data_list, key=lambda data: (data['upvotes'])))
  return render_template("read.html", subreddits = list_to_return, datas = data_list)

app.run(host="0.0.0.0")


#  post_containers = soup.find_all("div", {"data-testid": "post-container"})
# def get_link(soup):
#   link_list = []
#   links = soup.find_all("a", {"data-click-id": "timestamp"})
#   for link in links:
#     link_list.append(link.attrs['href'])
#   return link_list

# def get_upvotes(soup):
#   vote_list = []
#   upvotes = soup.find_all("div", {"style":"width:40px;border-left:4px solid transparent"})
#   #({"id":'vote-arrows-t3'})이 id 주소로 지정하면 왜 안찾아질까.. slack에 따르면 class가 blank인 div가 있으면 pass 되나보다
#   for upvote in upvotes:
#     a = upvote.get_text()
#     vote_list.append(a)
#   return vote_list

# def get_title(soup):
#   title_list = []
#   titles = soup.find_all("h3")
#   for title in titles:
#     title_list.append(title.text)
#   return title_list