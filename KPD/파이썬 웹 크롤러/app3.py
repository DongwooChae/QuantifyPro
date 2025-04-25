from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

검색어 = '맥도널 더글러스'
data = requests.get(f'https://ko.wikipedia.org/wiki/{검색어}')
soup = BeautifulSoup(data.content, 'html.parser')

# print(soup.find_all('span', class_=['value', 'yf-1jj98ts']))
# print(soup.select('span.value.yf-1jj98ts'))
print(soup.select('span.mw-page-title-main')[0].text)


# 구글 파이낸스 찾기
data2 = requests.get(f'https://www.google.com/finance/quote/COST:NASDAQ?hl=ko&comparison=')
# data2.status_code
# soup2 = BeautifulSoup(data2.content, 'html.parser')
# 전일종가 = soup2.find_all('div', class_="P6K39c").text
# print(전일종가)

if data2.status_code == 200:
    soup2 = BeautifulSoup(data2.content, 'html.parser')
    element = soup2.find_all('div', class_= 'P6K39c')[0].text
    print(element)
else:
    print('접속에 실패했습니다.')