import pandas as pd
from config import subject_template, mail_template, attachments, person_path, excel_path



df = pd.read_excel(excel_path, engine='openpyxl')

unique_persons = df['자료요청담당'].dropna().unique().tolist()



persons_series = pd.Series(unique_persons)
# print(persons_series)

selected_person = persons_series[persons_series.str.contains('채동우')]
valuation_person = persons_series[persons_series.str.contains('채동우')]

cond1 = df['자료요청담당'].isin(selected_person)
cond2 = df['재평가/신규'].str.contains('신규')
cond3 = df['평가종류코드'].str.contains('B01')
cond4 = df['평가담당자'].str.contains('채동우')

출력df = df[cond1&cond2&cond3]

print(출력df[['종목명', '평가담당자','자료요청담당','자료회신여부']])
# print(df[cond2&cond3&cond4])
