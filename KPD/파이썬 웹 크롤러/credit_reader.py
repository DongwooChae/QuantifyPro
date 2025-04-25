import pandas as pd

df = pd.read_csv('C:\\Users\\dwchae23\\QuantifyPro\\workplace\\KPD\\파이썬 웹 크롤러\\credit.csv')

print(df)

gender_male = df['성별'] == 'M'
married = df['기혼'] == 'Married'
not_married = df['기혼'] == 'Single'

# print(df[[gender_male & married]])

print(df.query(" 성별 == 'M' and 기혼 == 'Married' ")[['사용금액','사용횟수']].mean())
print(df.query(" 성별 == 'M' and 기혼 == 'Single' ")[['사용금액','사용횟수']].mean())

결혼한남자 = df.query(" 성별 == 'M' and 기혼 == 'Married' ")[['사용금액','사용횟수']].mean()
결혼안한남자 = df.query(" 성별 == 'M' and 기혼 == 'Single' ")[['사용금액','사용횟수']].mean()


if 결혼한남자['사용금액'] > 결혼안한남자['사용횟수'] :
    print('결혼한 남자의 사용금액 및 사용횟수가 더 높습니다.')
else :
    print('결혼 안한 남자가 돈 더 씀')

# print(df.query(" 성별 == 'M' and 기혼 == 'Married' ")[['나이','사용금액','사용횟수']].mean())
# print(df.query(" 성별 == 'M' and 기혼 == 'Single' ")[['나이','사용금액','사용횟수']].mean())

# print ((결혼한남자['사용금액'] / 결혼안한남자['사용금액'])- 1)

print(df.groupby('소득')[['나이','사용금액','사용횟수']].mean())