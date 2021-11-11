import requests
from bs4 import BeautifulSoup

def scrapper(term, headers):
  url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  result = requests.get(url, headers = headers)
  soup = BeautifulSoup(result.text, "html.parser")
  list_to_return = []
  articles = soup.find_all("article")
  for article in articles:
    lis = article.find_all("li")
    for li in lis:
      temp_link = li.find_all("a")#여기부터
      if len(temp_link) == 1:
        continue
      li = temp_link[1]#여기까지는 li 안의 a를 구분할 방법이 없어서 각 li의 2번째 a만 선택해주기 위한 프로그래밍
      temp = {}
      temp['title'] = li.find("span", {"class":"title"}).text
      temp['company'] = li.find("span", {"class":"company"}).text
      temp['link'] = "https://weworkremotely.com"+li.attrs['href']
      list_to_return.append(temp)
  return list_to_return