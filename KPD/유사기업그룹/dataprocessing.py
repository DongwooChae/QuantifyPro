# 라이브러리 import

import pandas as pd
import numpy as np

from loader import (df_company, df_kospi_group, df_kosdaq_group, df_kospi_company, df_kosdaq_company, price, fsdata)

# df_summary 데이터프레임 생성

df_summary = df_company[['10차표준(세분류)','10차표준(세세분류)','주요상품']].sort_values(by='10차표준(세분류)')
df_summary['KAP세분류'] = df_summary['10차표준(세분류)']

# 1) 칼럼을 꺼내서 별도 변수에 저장
KAP세분류 = df_summary.pop('KAP세분류')

# 2) 맨 앞(0번 인덱스)에 삽입
df_summary.insert(0, 'KAP세분류', KAP세분류)


# df_summary 분류 조정

df_summary.loc['제놀루션','KAP세분류'] = '인공지능(제약,바이오)'
df_summary.loc['제이엘케이','KAP세분류'] = '인공지능(제약,바이오)'
df_summary.loc['신테카바이오','KAP세분류'] = '인공지능(제약,바이오)'
df_summary.loc['딥노이드','KAP세분류'] = '인공지능(제약,바이오)'
df_summary.loc['핀텔','KAP세분류'] = '인공지능(일반)'
df_summary.loc['씨유박스','KAP세분류'] = '인공지능(일반)'
df_summary.loc['코난테크놀로지','KAP세분류'] = '인공지능(일반)'
df_summary.loc['모아데이타','KAP세분류'] = '인공지능(일반)'
df_summary.loc['바이브컴퍼니','KAP세분류'] = '인공지능(일반)'
df_summary.loc['셀바스AI','KAP세분류'] = '인공지능(일반)'
df_summary.loc['마음AI','KAP세분류'] = '인공지능(일반)'
df_summary.loc['위세아이텍','KAP세분류'] = '인공지능(일반)'
df_summary.loc['트윔','KAP세분류'] = '인공지능(일반)'
df_summary.loc['알체라','KAP세분류'] = '인공지능(일반)'
df_summary.loc['라온피플','KAP세분류'] = '인공지능(일반)'
df_summary.loc['크라우드웍스','KAP세분류'] = '인공지능(일반)'
df_summary.loc['솔트룩스','KAP세분류'] = '인공지능(일반)'

제조업 = df_summary['KAP세분류'].str.contains('제조업')
df_summary.loc[제조업,'KAP세분류'] = '제조업'

주조업 = df_summary['KAP세분류'].str.contains('주조')
df_summary.loc[주조업,'KAP세분류'] = '제조업'

건조업 = df_summary['KAP세분류'].str.contains('건조')
df_summary.loc[건조업,'KAP세분류'] = '제조업'

제재및목재가공업 = df_summary['KAP세분류'].str.contains('제재 및 목재 가공업')
df_summary.loc[제재및목재가공업,'KAP세분류'] = '제조업'

일반은행 = df_summary['KAP세분류'].str.contains('은행')
df_summary.loc[일반은행, 'KAP세분류'] = '서비스업'

금융업 = df_summary['KAP세분류'].str.contains('금융')
df_summary.loc[금융업,'KAP세분류'] = '금융업'

보험업 = df_summary['KAP세분류'].str.contains('보험')
df_summary.loc[보험업,'KAP세분류'] = '금융업'

저축업 = df_summary['KAP세분류'].str.contains('저축')
df_summary.loc[저축업,'KAP세분류'] = '금융업'

증권및선물중개업 = df_summary['KAP세분류'].str.contains('선물')
df_summary.loc[증권및선물중개업,'KAP세분류'] = '금융업'

신탁업및집합투자업 = df_summary['KAP세분류'].str.contains('신탁업 및 집합투자업')
df_summary.loc[신탁업및집합투자업,'KAP세분류'] = '금융업'

도매업 = df_summary['KAP세분류'].str.contains('도매')
df_summary.loc[도매업,'KAP세분류'] = '도매업'

건설업 = df_summary['KAP세분류'].str.contains('건설')
df_summary.loc[건설업,'KAP세분류'] = '건설업'

건축업 = df_summary['KAP세분류'].str.contains('건축')
df_summary.loc[건축업,'KAP세분류'] = '건설업'

공사업 = df_summary['KAP세분류'].str.contains('공사')
df_summary.loc[공사업, 'KAP세분류'] = '건설업'

운송업 = df_summary['KAP세분류'].str.contains('운송')
df_summary.loc[운송업,'KAP세분류'] = '운송업'

화물취급업 = df_summary['KAP세분류'].str.contains('화물 취급업')
df_summary.loc[화물취급업,'KAP세분류'] = '운송업'

소프트웨어서비스1 = df_summary['KAP세분류'].str.contains('컴퓨터시스템 통합 자문, 구축 및 관리업')
df_summary.loc[소프트웨어서비스1, 'KAP세분류'] = '소프트웨어서비스'

소프트웨어서비스2 = df_summary['KAP세분류'].str.contains('컴퓨터 프로그래밍, 시스템 통합 및 관리업')
df_summary.loc[소프트웨어서비스2, 'KAP세분류'] = '소프트웨어서비스'

게임업 = df_summary['KAP세분류'].str.contains('게임 소프트웨어 개발 및 공급업')
df_summary.loc[게임업, 'KAP세분류'] = '게임업'

방송업 = df_summary['KAP세분류'].str.contains('방송')
df_summary.loc[방송업, 'KAP세분류'] = '방송업'

영화및비디오물상영업 = df_summary['KAP세분류'].str.contains('영화 및 비디오물 상영업')
df_summary.loc[영화및비디오물상영업, 'KAP세분류'] = '방송업'

통신업 = df_summary['KAP세분류'].str.contains('통신')
df_summary.loc[통신업, 'KAP세분류'] = '통신업'

출판업 = df_summary['KAP세분류'].str.contains('출판')
df_summary.loc[출판업, 'KAP세분류'] = '출판업'

인쇄업 = df_summary['KAP세분류'].str.contains('인쇄')
df_summary.loc[인쇄업, 'KAP세분류'] = '출판업'

기록매체복제업 = df_summary['KAP세분류'].str.contains('기록매체 복제업')
df_summary.loc[기록매체복제업, 'KAP세분류'] = '출판업'

광고업 = df_summary['KAP세분류'].str.contains('광고')
df_summary.loc[광고업, 'KAP세분류'] = '광고업'

중개업 = df_summary['KAP세분류'].str.contains('중개')
df_summary.loc[중개업, 'KAP세분류'] = '광고업'

정보매개서비스업 = df_summary['KAP세분류'].str.contains('자료처리, 호스팅, 포털 및 기타 인터넷 정보매개 서비스업')
df_summary.loc[정보매개서비스업, 'KAP세분류'] = '소프트웨어서비스'

전문과학기술서비스업 = df_summary['KAP세분류'].str.contains('그 외 기타 전문, 과학 및 기술 서비스업')
df_summary.loc[전문과학기술서비스업, 'KAP세분류'] = '소프트웨어서비스'

경영컨설팅업 = df_summary['KAP세분류'].str.contains('경영 컨설팅 및 공공 관계 서비스업')
df_summary.loc[경영컨설팅업, 'KAP세분류'] = '소프트웨어서비스'

그외기타정보서비스업 = df_summary['KAP세분류'].str.contains('그 외 기타 정보 서비스업')
df_summary.loc[그외기타정보서비스업, 'KAP세분류'] = '소프트웨어서비스'

시스템소프트웨어개발및공급업 = df_summary['KAP세분류'].str.contains('시스템ㆍ응용 소프트웨어 개발 및 공급업')
df_summary.loc[시스템소프트웨어개발및공급업, 'KAP세분류'] = '소프트웨어서비스'

소프트웨어개발및공급업 = df_summary['KAP세분류'].str.contains('소프트웨어 개발 및 공급업')
df_summary.loc[소프트웨어개발및공급업, 'KAP세분류'] = '소프트웨어서비스'

기타정보서비스업 = df_summary['KAP세분류'].str.contains('기타 정보 서비스업')
df_summary.loc[기타정보서비스업, 'KAP세분류'] = '소프트웨어서비스'

소매업 = df_summary['KAP세분류'].str.contains('소매')
df_summary.loc[소매업, 'KAP세분류'] = '소매업'

연구개발업 = df_summary['KAP세분류'].str.contains('연구개발')
df_summary.loc[연구개발업, 'KAP세분류'] = '연구개발업'

기술시험검사및분석업 = df_summary['KAP세분류'].str.contains('기술 시험, 검사 및 분석업')
df_summary.loc[기술시험검사및분석업, 'KAP세분류'] = '연구개발업'

서비스업 = df_summary['KAP세분류'].str.contains('서비스업')
df_summary.loc[서비스업, 'KAP세분류'] = '서비스업'

일반교습학원 = df_summary['KAP세분류'].str.contains('일반 교습 학원')
df_summary.loc[일반교습학원, 'KAP세분류'] = '서비스업'

여행사업 = df_summary['KAP세분류'].str.contains('여행')
df_summary.loc[여행사업, 'KAP세분류'] = '서비스업'

개인및가정용품임대업 = df_summary['KAP세분류'].str.contains('개인 및 가정용품 임대업')
df_summary.loc[개인및가정용품임대업, 'KAP세분류'] = '서비스업'

부동산업 = df_summary['KAP세분류'].str.contains('부동산')
df_summary.loc[부동산업, 'KAP세분류'] = '부동산업'

일반및생활숙박시설운영업 = df_summary['KAP세분류'].str.contains('일반 및 생활 숙박시설 운영업')
df_summary.loc[일반및생활숙박시설운영업, 'KAP세분류'] = '부동산업'

골프장및스키장운영업 = df_summary['KAP세분류'].str.contains('골프장 및 스키장 운영업')
df_summary.loc[골프장및스키장운영업, 'KAP세분류'] = '부동산업'

자동차업 = df_summary['KAP세분류'].str.contains('자동차')
df_summary.loc[자동차업, 'KAP세분류'] = '자동차업'

육류업 = df_summary['KAP세분류'].str.contains('육류')
df_summary.loc[육류업, 'KAP세분류'] = '농축수임산물업'

채소업 = df_summary['KAP세분류'].str.contains('채소')
df_summary.loc[채소업, 'KAP세분류'] = '농축수임산물업'

작물업 = df_summary['KAP세분류'].str.contains('작물')
df_summary.loc[작물업, 'KAP세분류'] = '농축수임산물업'

어업 = df_summary['KAP세분류'].str.contains('어업')
df_summary.loc[어업, 'KAP세분류'] = '농축수임산물업'

수산동물가공및저장처리업 = df_summary['KAP세분류'].str.contains('수산동물 가공 및 저장 처리업')
df_summary.loc[수산동물가공및저장처리업, 'KAP세분류'] = '농축수임산물업'

수산물가공및저장처리업 = df_summary['KAP세분류'].str.contains('수산물 가공 및 저장 처리업')
df_summary.loc[수산물가공및저장처리업, 'KAP세분류'] = '농축수임산물업'

선박및수상부유구조물건조업 = df_summary['KAP세분류'].str.contains('선박 및 수상 부유 구조물 건조업')
df_summary.loc[선박및수상부유구조물건조업, 'KAP세분류'] = '제조업'

연료용가스제조및배관공급업 = df_summary['KAP세분류'].str.contains('연료용 가스 제조 및 배관공급업')
df_summary.loc[연료용가스제조및배관공급업, 'KAP세분류'] = '제조업'

금속열처리도금및기타금속가공업 = df_summary['KAP세분류'].str.contains('금속 열처리, 도금 및 기타 금속가공업')
df_summary.loc[금속열처리도금및기타금속가공업, 'KAP세분류'] = '제조업'

시장조사및여론조사업 = df_summary['KAP세분류'].str.contains('시장조사 및 여론조사업')
df_summary.loc[시장조사및여론조사업, 'KAP세분류'] = '서비스업'

전문디자인업 = df_summary['KAP세분류'].str.contains('전문 디자인업')
df_summary.loc[전문디자인업, 'KAP세분류'] = '서비스업'

초등학교 = df_summary['KAP세분류'].str.contains('초등')
df_summary.loc[초등학교, 'KAP세분류'] = '서비스업'

직원훈련 = df_summary['KAP세분류'].str.contains('직원')
df_summary.loc[직원훈련, 'KAP세분류'] = '서비스업'

사행시설관리및운영업 = df_summary['KAP세분류'].str.contains('사행시설 관리 및 운영업')
df_summary.loc[사행시설관리및운영업, 'KAP세분류'] = '서비스업'

지정폐기물처리업 = df_summary['KAP세분류'].str.contains('지정 폐기물 처리업')
df_summary.loc[지정폐기물처리업, 'KAP세분류'] = '서비스업'

석유정제물재처리업 = df_summary['KAP세분류'].str.contains('석유 정제물 재처리업')
df_summary.loc[석유정제물재처리업, 'KAP세분류'] = '서비스업'

원유정제처리업 = df_summary['KAP세분류'].str.contains('원유 정제처리업')
df_summary.loc[원유정제처리업, 'KAP세분류'] = '서비스업'

해체선별및원료재생업 = df_summary['KAP세분류'].str.contains('해체, 선별 및 원료 재생업')
df_summary.loc[해체선별및원료재생업, 'KAP세분류'] = '서비스업'

직물직조업 = df_summary['10차표준(세분류)'].str.contains('직물 직조업')
df_summary.loc[직물직조업, 'KAP세분류'] = '서비스업'

증기냉온수및공기조절공급업 = df_summary['10차표준(세분류)'].str.contains('증기, 냉ㆍ온수 및 공기조절 공급업')
df_summary.loc[증기냉온수및공기조절공급업, 'KAP세분류'] = '서비스업'

전기업 = df_summary['10차표준(세분류)'].str.contains('전기업')
df_summary.loc[전기업, 'KAP세분류'] = '서비스업'

기관구내식당업 = df_summary['10차표준(세분류)'].str.contains('기관 구내식당업')
df_summary.loc[기관구내식당업, 'KAP세분류'] = '서비스업'

산업용기계및장비임대업 = df_summary['10차표준(세분류)'].str.contains('산업용 기계 및 장비 임대업')
df_summary.loc[산업용기계및장비임대업, 'KAP세분류'] = '서비스업'

음식점업 = df_summary['10차표준(세분류)'].str.contains('음식점업')
df_summary.loc[음식점업, 'KAP세분류'] = '서비스업'

섬유제품염색정리및마무리가공업 = df_summary['10차표준(세분류)'].str.contains('섬유제품 염색, 정리 및 마무리 가공업')
df_summary.loc[섬유제품염색정리및마무리가공업, 'KAP세분류'] = '서비스업'

송전및배전업 = df_summary['10차표준(세분류)'].str.contains('송전 및 배전업')
df_summary.loc[송전및배전업, 'KAP세분류'] = '서비스업'

회사본부 = df_summary['KAP세분류'].str.contains('회사 본부')
df_summary.loc[회사본부,'KAP세분류'] = '지주회사'

스팩 = df_summary.index.get_level_values('종목명').str.contains('스팩')
df_summary.loc[스팩,'KAP세분류'] = '스팩'

# KAP세분류 열을 카테고리 자료형으로 변환
df_summary['KAP세분류'] = df_summary['KAP세분류'].astype('category')