import requests
import json
from bs4 import BeautifulSoup

data = requests.get('https://finance.yahoo.com/quote/COST/')
soup = BeautifulSoup(data.content, 'html.parser')
price = soup.find_all('span', id = "qsp-price")
company_name = soup.find_all('h1', class_ ="yf-xxbei9")


# 네이버 증권 동일업종 등락률 찾기
data2 = requests.get('https://finance.naver.com/item/main.naver?code=214150')
soup2 = BeautifulSoup(data2.content, 'html.parser')
print(soup2.find_all('em', id="_per")[0].text)


price2 = soup2.select('.f_up em')[1].text
print(price2)

# print(price2[0].text)

# print(soup.select('h1yf-xxbei9')[0].text)

# print(soup.select('.yf-xxbei9'))
# print(soup.select('span#qsp-price'))



# company_label = soup2.find_all('div', class_="info_group")[2].text





# print(data.content)
