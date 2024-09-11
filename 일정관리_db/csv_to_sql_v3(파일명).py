import pandas as pd
import os

# CSV 파일 경로
csv_file = r'C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db\KAP_일정관리\db_csv\20240910_db.csv'

# CSV 파일 이름에서 날짜 부분 추출
file_name = os.path.basename(csv_file)  # 파일명만 추출 (예: 20240909_db.csv)
date_part = file_name.split('_')[0]  # 첫 번째 부분인 날짜 (예: 20240909)

# 데이터프레임으로 CSV 파일 읽기
try:
    df = pd.read_csv(csv_file, encoding='utf-8')  # 필요한 경우 인코딩 변경
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# 테이블 및 열 이름 지정
table_name = '종목관리대장'
columns = df.columns.tolist()

# INSERT 문 생성
insert_statements = []
for index, row in df.iterrows():
    values = []
    for value in row.tolist():
        if pd.isna(value):  # NaN 값 처리
            values.append('NULL')
        elif isinstance(value, str):
            values.append('"' + value.replace('"', '""') + '"')  # 따옴표 처리
        else:
            values.append(str(value))
    insert_statement = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join(values)});'
    insert_statements.append(insert_statement)


output_file = fr'C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db\KAP_일정관리\insert_statements_{date_part}.sql'

# INSERT 문 파일로 저장 (지정된 경로 및 CSV 파일의 날짜를 사용한 파일명)
output_file = fr'C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db\KAP_일정관리\Table_Query\insert_statements_{date_part}.sql'

try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for statement in insert_statements:
            f.write(statement + '\n')
    print(f"성공적으로 저장되었습니다: {output_file}")
except Exception as e:
    print(f"Error writing SQL file: {e}")