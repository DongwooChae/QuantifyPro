import pandas as pd

# CSV 파일 경로
csv_file = r'C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db\KAP_일정관리\db_csv\20240905_db.csv'
# save_csv = r"C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db\inster_statements.sql"
# C:\Users\dwchae23\QuantifyPro\workplace\일정관리_db\KAP_일정관리\db_csv\20240905_db.csv

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

# INSERT 문 파일로 저장
try:
    with open(r'C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db\KAP_일정관리\insert_statements.sql', 'w', encoding='utf-8') as f:
        for statement in insert_statements:
            f.write(statement + '\n')
    print("성공적으로 저장되었습니다.")
except Exception as e:
    print(f"Error writing SQL file: {e}")

# C:/Users/User/Desktop/KAP_일정관리/insert_statements.sql
# C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db/inster_statements.sql