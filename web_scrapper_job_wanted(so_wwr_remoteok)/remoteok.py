import requests
from bs4 import BeautifulSoup

def scrapper(term, headers):
  url = f"https://remoteok.io/remote-dev+{term}-jobs"
  result = requests.get(url, headers = headers)
  soup = BeautifulSoup(result.text, "html.parser")
  tds = soup.find_all("td", {"class":"company position company_and_position"})
  list_to_return = []
  for td in tds[1:]:#thead에서 골라진 td 제외
    if td.find("span", {"class":"closed tooltip"}):
      continue
    else:
        temp = {}
        temp['title'] = td.find("h2").text
        temp['company'] = td.find("h3").text
        temp_link = td.find("a", {"itemprop":"url"})
        temp['link'] = "https://remoteok.io"+temp_link.attrs['href']
        list_to_return.append(temp)
  return list_to_return
