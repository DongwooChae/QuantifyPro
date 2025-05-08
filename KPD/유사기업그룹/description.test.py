import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# 1) 입력 파일에서 symbol 리스트 읽어오기
infile = 'Template_ComparableCompany_copy2.xlsx'
df_codes = pd.read_excel(infile, sheet_name=0, usecols=['symbol'])
symbols = df_codes['symbol'].dropna().tolist()

# 상위 10개만 사용
symbols = symbols[:10]

# 2) 크롤링해서 결과 수집
rows = []
for code in symbols:
    url = (
        'https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp'
        f'?pGB=1&gicode={code}&cID=AA&MenuYn=Y'
        '&ReportGB=&NewMenuID=11&stkGb=701'
    )
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, 'lxml')

    title = (soup.find_all('h3', id='bizSummaryHeader')[0].text)
    content = (soup.find_all('ul', id='bizSummaryContent')[0])
    full_content = content.get_text(separator='\n\n', strip=True)

    rows.append({
        'symbol':      code,
        'description': f"{title}\n\n{full_content}"
    })
    print(f"{code} 크롤링 완료")

# 3) DataFrame으로 만들고 새 엑셀로 저장
df_out = pd.DataFrame(rows)

with pd.ExcelWriter('company_code_parsed_top10.xlsx', engine='xlsxwriter') as writer:
    df_out.to_excel(writer, index=False, sheet_name='Sheet1')
    wb = writer.book
    ws = writer.sheets['Sheet1']

    # A열(symbol) 넓이, B열(description)에 자동줄바꿈 설정
    wrap_fmt = wb.add_format({'text_wrap': True})
    ws.set_column('A:A', 12)
    ws.set_column('B:B', 60, wrap_fmt)

print("✅ 상위 10개만 저장한 'company_code_parsed_top10.xlsx' 생성 완료!")
