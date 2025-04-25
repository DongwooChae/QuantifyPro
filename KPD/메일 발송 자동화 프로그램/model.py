from reader import load_requests, load_contacts
import pandas as pd

def get_unique_requesters() -> list[str]:
    df = load_requests()
    # NA 제거, 중복 제거, 정렬
    users = df['자료요청담당'].dropna().unique().tolist()
    return sorted(users)


df = load_requests()
print(df.info())

users = df['자료요청담당'].dropna().unique().tolist()
print(users)

cond1 = df['자료요청담당'].str.contains('채동우')
cond2 = df['재평가/신규'].str.contains('신규')
cond3 = df['평가종류코드'].str.contains('B01') # 펀드

df_filtered = df[cond1 & cond2 & cond3]
print(df_filtered)