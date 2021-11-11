import math
import requests
from bs4 import BeautifulSoup


so_url = "https://stackoverflow.com/jobs?r=true"

def get_html(url, headers):
  result = requests.get(url, headers = headers)
  soup = BeautifulSoup(result.text, "html.parser")
  return soup

def get_last_page(term, headers):
  url = f"{so_url}&q={term}"
  soup = get_html(url, headers)
  job_count = soup.find("span", {"class":"description fc-light fs-body1"}).text.replace("jobs","").strip()
  job_count = int(job_count)
  if job_count == '0':#그냥 올림으로만 하면 아무것도 없을 때 max_page가 0이 되어버린다.
    last_page = 1
  else:
    last_page = math.ceil(int(job_count)/25)
  return last_page
# 이 코드로 짜면 실제 페이지 출력보다 더 많이 나온다 ;; 



def scrapper(term, headers):
  last_page = get_last_page(term, headers)
  list_to_return = []
  for page_number in range(1, last_page+1):
    url = f"{so_url}&q={term}&pg={page_number}"
    soup = get_html(url, headers)
    results_list = soup.find("div", {"class":"listResults"})
    items = results_list.find_all("div", {"class":"flex--item fl1"})
    for item in items:
      temp = {}
      link = item.find("a", {"class":"s-link stretched-link"})
      temp['title'] = link.text
      temp['company'] = item.find("h3", {"class":"fc-black-700 fs-body1 mb4"}).find("span").text.strip()
      temp['link'] = "https://stackoverflow.com/"+link.attrs['href']
      list_to_return.append(temp)
  return list_to_return