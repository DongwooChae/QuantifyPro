import requests
from bs4 import BeautifulSoup
import selenium

# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

var = requests.get('https://finance.naver.com/item/sise.nhn?code=005930')
var2 = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blhI&pkid=594&os=15137208&qvt=0&query=%ED%95%9C%EA%B5%AD%EC%9E%90%EC%82%B0%ED%8F%89%EA%B0%80(%EC%A3%BC)')
var3 = requests.get('https://www.nicebizline.com/workspace/CO001/t4Gf')

soup3 = BeautifulSoup(var3.content, 'html.parser')
company_label3 = soup3.find_all('button', a_="btn--text btn--small btn--underline line1 secondary")
company_label4 = soup3.find_all('#text')

print(company_label3)
print(company_label4)

soup2 = BeautifulSoup(var2.content, 'html.parser')
company_label = soup2.find_all('div', class_="info_group")[2].text
print(company_label)


# print(var.content)
# print(var.status_code)
soup = BeautifulSoup(var.content, 'html.parser')

# print(soup)

# print(soup.find_all('span', class_="tah")[0].text) # 찾은 결과는 리스트 []로 뱉어줌, 컴퓨터야 HTML 중에서 <strong>인데 class="tah p11"인 것 찾아줘
# print(soup.find_all('span', id="_quant")[0].text) # 찾은 결과는 리스트 []로 뱉어줌, 컴퓨터야 HTML 중에서 <strong>인데 class="tah p11"인 것 찾아줘

# # print(soup.find_all('strong', id = '_nowVal')[0]) # 따라서 인덱싱을 통해 값 자체를 뽑아와야 함
# print(soup.find_all('strong', id = '_nowVal')[0].text) # 값 자체를 가져오려면 .text

