import pandas as pd
import os

# CSV 파일들이 있는 폴더 경로
# folder_path = r'C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db\KAP_일정관리\db_csv_group'

# 회사 컴퓨터로 작업 시 아래 디렉토리 적용
folder_path = r'C:\Users\dwchae23\QuantifyPro\workplace\일정관리_db\KAP_일정관리\db_csv_group'

# 최종 SQL 파일 저장 경로
# output_file = r'C:\Users\User\Documents\GitHub\QuantifyPro\일정관리_db\KAP_일정관리\Table_Query\insert_statements_combined.sql'

# 회사 컴퓨터로 작업 시 아래 디렉토리 적용
output_file = r'C:\Users\dwchae23\QuantifyPro\workplace\일정관리_db\KAP_일정관리\Table_Query\insert_statements_combined.sql'

# SQL 파일을 미리 열어둠 (쓰기 모드로 시작)
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        # 폴더 내의 모든 CSV 파일 처리
        for csv_file in os.listdir(folder_path):
            if csv_file.endswith('.csv'):
                # 전체 경로
                full_path = os.path.join(folder_path, csv_file)

                # CSV 파일 이름에서 날짜 부분 추출
                file_name = os.path.basename(full_path)  # 파일명만 추출 (예: 20240909_db.csv)
                date_part = file_name.split('_')[0]  # 첫 번째 부분인 날짜 (예: 20240909)

                # 데이터프레임으로 CSV 파일 읽기
                try:
                    df = pd.read_csv(full_path, encoding='utf-8')  # 필요한 경우 인코딩 변경
                except Exception as e:
                    print(f"Error reading CSV file {csv_file}: {e}")
                    continue  # 에러 발생 시 다음 파일로 넘어감

                # 테이블 및 열 이름 지정
                table_name = '종목관리대장'
                columns = df.columns.tolist()

                # INSERT 문 생성
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
                    
                    # SQL 파일에 INSERT 문 추가
                    f.write(insert_statement + '\n')

        print(f"모든 SQL INSERT 문이 성공적으로 {output_file}에 저장되었습니다.")
except Exception as e:
    print(f"Error writing SQL file: {e}")
