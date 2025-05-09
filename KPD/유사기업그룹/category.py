# 라이브러리 import

import pandas as pd
import numpy as np

from loader import (df_company, df_kospi_group, df_kosdaq_group, df_kospi_company, df_kosdaq_company, price, fsdata, category, category_company)

# dtype 변환
dtype_col = ['Sector','Industry Group','Industry', '10차표준(세분류)', '10차표준(세세분류)','주요상품']
category_company[dtype_col] = category_company[dtype_col].astype('string')

세분류에너지 = category_company['10차표준(세분류)'].str.contains('에너지')
세분류석유 = category_company['10차표준(세분류)'].str.contains('석유')
세분류가스= category_company['10차표준(세분류)'].str.contains('가스')
에너지 = 세분류에너지 | 세분류석유 | 세분류가스
category_company.loc[에너지, 'Industry'] = '에너지 시설 및 서비스, 석유 및 가스'

세분류화학 = category_company['10차표준(세분류)'].str.contains('화학')
세분류건축소재 = category_company['10차표준(세분류)'].str.contains(r'건축소재')
세분류용기및포장 = category_company['10차표준(세분류)'].str.contains(r'용기|포장')
세분류금속및광물 = category_company['10차표준(세분류)'].str.contains(r'금속|광물')
세분류종이및목재 = category_company['10차표준(세분류)'].str.contains(r'종이|목재')
소재 = 세분류화학|세분류건축소재|세분류용기및포장|세분류금속및광물|세분류종이및목재
category_company.loc[소재, 'Industry'] = '화학, 건축소재, 용기 및 포장, 금속 및 광물, 종이 및 목재'

세분류건축자재 = category_company['10차표준(세분류)'].str.contains(r'건축|자재')
세분류플라스틱 = category_company['10차표준(세분류)'].str.contains(r'플라스틱')
세분류건설 = category_company['10차표준(세분류)'].str.contains('건설')
세분류핵반응기 = category_company['10차표준(세분류)'].str.contains('핵반응기')
세분류항공기 = category_company['10차표준(세분류)'].str.contains('항공기')
세분류우주선 = category_company['10차표준(세분류)'].str.contains('우주선')
세분류전자부품 = category_company['10차표준(세분류)'].str.contains(r'전자부품')
세분류전기장비 = category_company['10차표준(세분류)'].str.contains(r'전기장비|전기')
세분류철강 = category_company['10차표준(세분류)'].str.contains(r'철강')
세분류복합산업 = category_company['10차표준(세분류)'].str.contains('복합산업')
세분류기계 = category_company['10차표준(세분류)'].str.contains('기계')
세분류무역 = category_company['10차표준(세분류)'].str.contains('무역')
세분류조선 = category_company['10차표준(세분류)'].str.contains('조선')
세분류시멘트 = category_company['10차표준(세분류)'].str.contains('시멘트')
세분류엔지니어링 = category_company['10차표준(세분류)'].str.contains('엔지니어링')
세분류콘크리트 = category_company['10차표준(세분류)'].str.contains('콘크리트')
자본재 = 세분류건축자재|세분류건설|세분류전기장비|세분류복합산업|세분류기계|세분류무역|세분류조선|세분류철강|세분류전자부품 |세분류시멘트 |세분류엔지니어링 |세분류콘크리트 |세분류항공기|세분류우주선|세분류핵반응기|세분류플라스틱
category_company.loc[자본재, 'Industry'] = '건축자재, 건설, 전기장비, 복합 산업, 기계, 무역, 조선'

세분류상업서비스 = category_company['10차표준(세분류)'].str.contains('상업')
세세분류상업서비스 = category_company['10차표준(세세분류)'].str.contains('상업')
주요상품상업서비스 = category_company['주요상품'].str.contains('상업')
상업서비스 = 세분류상업서비스 | 세세분류상업서비스 | 주요상품상업서비스

category_company.loc[세분류상업서비스, 'Industry'] = '상업서비스'

세분류운송 = category_company['10차표준(세분류)'].str.contains(r'운송')
category_company.loc[세분류운송, 'Industry'] = '운송'

세분류자동차 = category_company['10차표준(세분류)'].str.contains(r'자동차')
category_company.loc[세분류자동차, 'Industry'] = '자동차'

세분류내구소비재 = category_company['10차표준(세분류)'].str.contains(r'내구소비재')
세분류레저용품 = category_company['10차표준(세분류)'].str.contains(r'레저')
세분류겉옷 = category_company['10차표준(세분류)'].str.contains(r'겉옷')
세분류섬유및의복 = category_company['10차표준(세분류)'].str.contains(r'섬유|의복')
내구소비재및의류 = 세분류내구소비재 | 세분류레저용품 | 세분류섬유및의복 | 세분류겉옷
category_company.loc[내구소비재및의류, 'Industry'] = '내구소비재, 레저용품, 섬유 및 의복'

세분류호텔및레저 = category_company['10차표준(세분류)'].str.contains(r'호텔|레저')
세분류교육 = category_company['10차표준(세분류)'].str.contains(r'교육')
소비자서비스 = 세분류호텔및레저 | 세분류교육
category_company.loc[소비자서비스, 'Industry'] = '호텔 및 레저, 교육'

세분류미디어 = category_company['10차표준(세분류)'].str.contains(r'미디어')
세세분류미디어 = category_company['10차표준(세세분류)'].str.contains(r'미디어')
주요상품미디어 = category_company['주요상품'].str.contains(r'미디어')
미디어 = 세분류미디어 | 세세분류미디어 | 주요상품미디어
category_company.loc[미디어, 'Industry'] = '미디어'

세분류도매및소매 = category_company['10차표준(세분류)'].str.contains(r'도매|소매')
주요상품온라인쇼핑 = category_company['주요상품'].str.contains(r'쇼핑')
주요상품백화점 = category_company['주요상품'].str.contains(r'백화점')
유동 = 세분류도매및소매 | 주요상품온라인쇼핑 | 주요상품백화점
category_company.loc[유동, 'Industry'] = '도매 및 소매, 온라인 쇼핑, 백화점'

세분류음료 = category_company['10차표준(세분류)'].str.contains(r'음료')
세분류동물용 = category_company['10차표준(세분류)'].str.contains(r'동물용')
세분류떡 = category_company['10차표준(세분류)'].str.contains(r'떡')
세분류식료품 = category_company['10차표준(세분류)'].str.contains(r'식료품')
세분류담배 = category_company['10차표준(세분류)'].str.contains(r'담배')
음식료및담배 = 세분류음료 | 세분류식료품 | 세분류담배 | 세분류동물용 | 세분류떡
category_company.loc[음식료및담배, 'Industry'] = '음료, 식료품, 담배'

세분류생활용품 = category_company['10차표준(세분류)'].str.contains(r'생활용품')
세분류세제 = category_company['10차표준(세분류)'].str.contains(r'세제')
세분류속옷 = category_company['10차표준(세분류)'].str.contains(r'속옷')
세세분류생활용품 = category_company['10차표준(세세분류)'].str.contains(r'생활용품')
주요상품생활용품 = category_company['주요상품'].str.contains(r'생활용품')

생활용품 = 세분류생활용품 | 세세분류생활용품 | 주요상품생활용품 | 세분류세제 | 세분류속옷
category_company.loc[생활용품, 'Industry'] = '생활용품'

세분류의료장비 = category_company['10차표준(세분류)'].str.contains(r'의료장비|의료기기')
세분류의료용품 = category_company['10차표준(세분류)'].str.contains(r'의료용품')
세분류의료용기기 = category_company['10차표준(세분류)'].str.contains(r'의료용기기|의료용 기기')
세세분류의료장비 = category_company['10차표준(세세분류)'].str.contains(r'의료장비|의료기기')
주요상품의료장비 = category_company['주요상품'].str.contains(r'의료장비|의료기기')
의료장비및서비스 = 세분류의료장비 | 세세분류의료장비 | 주요상품의료장비 | 세분류의료용품 | 세분류의료용기기
category_company.loc[의료장비및서비스, 'Industry'] = '의료장비 및 서비스'

세분류바이오 = category_company['10차표준(세분류)'].str.contains(r'바이오')
세분류의약 = category_company['10차표준(세분류)'].str.contains(r'의약')
세분류제약 = category_company['10차표준(세분류)'].str.contains(r'제약')
세세분류바이오 = category_company['10차표준(세세분류)'].str.contains(r'바이오')
세세분류의학 = category_company['10차표준(세세분류)'].str.contains(r'의학')
세세분류제약 = category_company['10차표준(세세분류)'].str.contains(r'제약')
주요상품바이오 = category_company['주요상품'].str.contains(r'바이오')
주요상품제약 = category_company['주요상품'].str.contains(r'제약')
제약및바이오 = 세분류바이오| 세분류의약 | 세분류제약 | 세세분류바이오 | 세세분류제약 | 세세분류의학 | 주요상품바이오 | 주요상품제약
category_company.loc[제약및바이오, 'Industry'] = '제약 및 바이오'

세분류은행 = category_company['10차표준(세분류)'].str.contains(r'은행')
세세분류은행 = category_company['10차표준(세세분류)'].str.contains(r'은행')
주요상품은행 = category_company['주요상품'].str.contains(r'은행')
은행 = 세분류은행 | 세세분류은행 | 주요상품은행
category_company.loc[은행, 'Industry'] = '은행'

세분류보험 = category_company['10차표준(세분류)'].str.contains(r'보험')
세세분류보험 = category_company['10차표준(세세분류)'].str.contains(r'보험')
주요상품보험 = category_company['주요상품'].str.contains(r'보험')
보험 = 세분류보험 | 세세분류보험 | 주요상품보험
category_company.loc[보험, 'Industry'] = '보험'

세분류증권 = category_company['10차표준(세분류)'].str.contains(r'증권')
세세분류증권 = category_company['10차표준(세세분류)'].str.contains(r'증권')
주요상품증권 = category_company['주요상품'].str.contains(r'증권')
증권 = 세분류증권 | 세세분류증권 | 주요상품증권
category_company.loc[증권, 'Industry'] = '증권'

세분류인터넷서비스 = category_company['10차표준(세분류)'].str.contains(r'인터넷')
세분류IT서비스 = category_company['10차표준(세분류)'].str.contains(r'IT')
세분류일반소프트웨어 = category_company['10차표준(세분류)'].str.contains(r'소프트웨어')
세분류게임소프트웨어 = category_company['10차표준(세분류)'].str.contains(r'게임')
소프트웨어 = 세분류인터넷서비스 | 세분류IT서비스 | 세분류일반소프트웨어 | 세분류게임소프트웨어
category_company.loc[소프트웨어, 'Industry'] = '인터넷 서비스, IT 서비스, 일반 소프트웨어, 게임 소프트웨어'

세분류IT하드웨어 = category_company['10차표준(세분류)'].str.contains(r'통신장비|휴대폰|셋톱|컴퓨터|보안장비|사무기기|전자장비')
세세분류IT하드웨어 = category_company['10차표준(세세분류)'].str.contains(r'통신장비|휴대폰|셋톱|컴퓨터|보안장비|사무기기|전자장비')
주요상품IT하드웨어 = category_company['주요상품'].str.contains(r'통신장비|휴대폰|셋톱|컴퓨터|보안장비|사무기기|전자장비')
IT하드웨어 = 세분류IT하드웨어 | 세세분류IT하드웨어 | 주요상품IT하드웨어
category_company.loc[IT하드웨어, 'Industry'] = 'IT 하드웨어'

세분류반도체및관련장비 = category_company['10차표준(세분류)'].str.contains(r'반도체|반도체장비')
세분류일차전지 = category_company['10차표준(세분류)'].str.contains(r'일차전지|이차전지')
세분류전자집적회로 = category_company['10차표준(세분류)'].str.contains(r'전자집적회로')
세분류측정 = category_company['10차표준(세분류)'].str.contains(r'측정|향해')
세세분류반도체및관련장비 = category_company['10차표준(세세분류)'].str.contains(r'반도체|반도체장비')
주요상품반도체및관련장비 = category_company['주요상품'].str.contains(r'반도체|반도체장비')
반도체및관련장비 = 세분류반도체및관련장비 | 세세분류반도체및관련장비 | 주요상품반도체및관련장비 |세분류일차전지|세분류전자집적회로|세분류측정
category_company.loc[반도체및관련장비, 'Industry'] = '반도체 및 관련 장비'

세분류디스플레이및관련부품 = category_company['10차표준(세분류)'].str.contains(r'디스플레이')
세세분류디스플레이및관련부품 = category_company['10차표준(세세분류)'].str.contains(r'디스플레이')
주요상품디스플레이및관련부품 = category_company['주요상품'].str.contains(r'디스플레이')
디스플레이및관련부품 = 세분류디스플레이및관련부품 | 세세분류디스플레이및관련부품 | 주요상품디스플레이및관련부품
category_company.loc[디스플레이및관련부품, 'Industry'] = '디스플레이 및 관련 부품'

세분류통신 = category_company['10차표준(세분류)'].str.contains(r'통신')
세분류정보서비스업 = category_company['10차표준(세분류)'].str.contains(r'정보 서비스업')
세분류광고 = category_company['10차표준(세분류)'].str.contains(r'광고')
세세분류통신 = category_company['10차표준(세세분류)'].str.contains(r'통신')
주요상품통신 = category_company['주요상품'].str.contains(r'통신')
통신서비스 = 세분류통신 | 세세분류통신 | 주요상품통신 | 세분류광고 | 세분류정보서비스업
category_company.loc[통신서비스, 'Industry'] = '유선통신, 무선통신'

세분류유틸리티 = category_company['10차표준(세분류)'].str.contains(r'전력|가스')
세세분류유틸리티 = category_company['10차표준(세세분류)'].str.contains(r'전력|가스')
주요상품유틸리티 = category_company['주요상품'].str.contains(r'전력|가스')
유틸리티 = 세분류유틸리티 | 세세분류유틸리티 | 주요상품유틸리티
category_company.loc[유틸리티, 'Industry'] = '유틸리티'

세분류부동산 = category_company['10차표준(세분류)'].str.contains(r'부동산')
세분류골프장 = category_company['10차표준(세분류)'].str.contains(r'골프장|스키장')
세세분류부동산 = category_company['10차표준(세세분류)'].str.contains(r'부동산')
주요상품부동산 = category_company['주요상품'].str.contains(r'부동산')
부동산 = 세분류부동산 | 세세분류부동산 | 주요상품부동산 | 세분류골프장
category_company.loc[부동산, 'Industry'] = '부동산'

인더스트리그룹에너지 = category_company['Industry'].str.contains('에너지 시설 및 서비스, 석유 및 가스')
인더스트리그룹소재 = category_company['Industry'].str.contains('화학, 건축소재, 용기 및 포장, 금속 및 광물, 종이 및 목재')
인더스트리그룹자본재 = category_company['Industry'].str.contains('건축자재, 건설, 전기장비, 복합 산업, 기계, 무역, 조선')
인더스트리그룹상업서비스 = category_company['Industry'].str.contains('상업서비스')
인더스트리그룹운송 = category_company['Industry'].str.contains('운송')
인더스트리그룹자동차및부품 = category_company['Industry'].str.contains('자동차')
인더스트리그룹내구소비재및의류 = category_company['Industry'].str.contains('내구소비재, 레저용품, 섬유 및 의복')
인더스트리그룹소비자서비스 = category_company['Industry'].str.contains('호텔 및 레저, 교육')
인더스트리그룹미디어 = category_company['Industry'].str.contains('미디어')
인더스트리그룹유통 = category_company['Industry'].str.contains('도매 및 소매, 온라인 쇼핑, 백화점')
인더스트리그룹음식료및담배 = category_company['Industry'].str.contains('음료, 식료품, 담배')
인더스트리그룹생활용품 = category_company['Industry'].str.contains('생활용품')
인더스트리그룹의료장비및서비스 = category_company['Industry'].str.contains('의료장비 및 서비스')
인더스트리그룹제약및바이오 = category_company['Industry'].str.contains('제약 및 바이오')
인더스트리그룹은행 = category_company['Industry'].str.contains('은행')
인더스트리그룹보험 = category_company['Industry'].str.contains('보험')
인더스트리그룹증권 = category_company['Industry'].str.contains('증권')
인더스트리그룹소프트웨어 = category_company['Industry'].str.contains('인터넷 서비스, IT 서비스, 일반 소프트웨어, 게임 소프트웨어')
인더스트리IT하드웨어 = category_company['Industry'].str.contains('IT 하드웨어')
인더스트리그룹반도체및관련장비 = category_company['Industry'].str.contains('반도체 및 관련 장비')
인더스트리그룹디스플레이및관련부품 = category_company['Industry'].str.contains('디스플레이 및 관련 부품')
인더스트리그룹통신서비스 = category_company['Industry'].str.contains('통신')
인더스트리그룹유틸리티 = category_company['Industry'].str.contains('유틸리티')
인더스트리그룹부동산 = category_company['Industry'].str.contains('부동산')

category_company.loc[인더스트리그룹에너지,'Industry Group'] = '에너지'
category_company.loc[인더스트리그룹소재,'Industry Group'] = '소재'
category_company.loc[인더스트리그룹자본재,'Industry Group'] = '자본재'
category_company.loc[인더스트리그룹상업서비스,'Industry Group'] = '상업서비스'
category_company.loc[인더스트리그룹운송,'Industry Group'] = '운송'
category_company.loc[인더스트리그룹자동차및부품,'Industry Group'] = '자동차 및 부품'
category_company.loc[인더스트리그룹내구소비재및의류,'Industry Group'] = '내구 소비재 및 의류'
category_company.loc[인더스트리그룹소비자서비스,'Industry Group'] = '소비자 서비스'
category_company.loc[인더스트리그룹미디어,'Industry Group'] = '미디어'
category_company.loc[인더스트리그룹유통,'Industry Group'] = '유통'
category_company.loc[인더스트리그룹음식료및담배,'Industry Group'] = '음식료 및 담배'
category_company.loc[인더스트리그룹생활용품,'Industry Group'] = '생활용품'
category_company.loc[인더스트리그룹의료장비및서비스,'Industry Group'] = '의료장비 및 서비스'
category_company.loc[인더스트리그룹제약및바이오,'Industry Group'] = '제약 및 바이오'
category_company.loc[인더스트리그룹은행,'Industry Group'] = '은행'
category_company.loc[인더스트리그룹보험,'Industry Group'] = '보험'
category_company.loc[인더스트리그룹증권,'Industry Group'] = '증권'
category_company.loc[인더스트리그룹소프트웨어,'Industry Group'] = '소프트웨어'
category_company.loc[인더스트리IT하드웨어,'Industry Group'] = '하드웨어'
category_company.loc[인더스트리그룹반도체및관련장비,'Industry Group'] = '반도체'
category_company.loc[인더스트리그룹디스플레이및관련부품,'Industry Group'] = '디스플레이'
category_company.loc[인더스트리그룹통신서비스,'Industry Group'] = '통신서비스'
category_company.loc[인더스트리그룹유틸리티,'Industry Group'] = '유틸리티'
category_company.loc[인더스트리그룹부동산,'Industry Group'] = '부동산'

섹터에너지 = category_company['Industry Group'] == '에너지'
섹터소재 = category_company['Industry Group'] == '소재'
섹터자본재 = category_company['Industry Group'] == '자본재'
섹터상업서비스 = category_company['Industry Group'] == '상업서비스'
섹터운송 = category_company['Industry Group'] == '운송'
섹터자동차및부품 = category_company['Industry Group'] == '자동차 및 부품'
섹터내구소비재및의류 = category_company['Industry Group'] == '내구 소비재 및 의류'
섹터소비자서비스 = category_company['Industry Group'] == '소비자 서비스'
섹터미디어 = category_company['Industry Group'] == '미디어'
섹터유통 = category_company['Industry Group'] == '유통'
섹터음식료및담배 = category_company['Industry Group'] == '음식료 및 담배'
섹터생활용품 = category_company['Industry Group'] == '생활용품'
섹터의료장비및서비스 = category_company['Industry Group'] == '의료장비 및 서비스'
섹터제약및바이오 = category_company['Industry Group'] == '제약 및 바이오'
섹터은행 = category_company['Industry Group'] == '은행'
섹터보험 = category_company['Industry Group'] == '보험'
섹터증권 = category_company['Industry Group'] == '증권'
섹터소프트웨어 = category_company['Industry Group'] == '소프트웨어'
섹터IT하드웨어 = category_company['Industry Group'] == '하드웨어'
섹터반도체 = category_company['Industry Group'] == '반도체'
섹터디스플레이 = category_company['Industry Group'] == '디스플레이'
섹터통신서비스 = category_company['Industry Group'] == '통신서비스'
섹터유틸리티 = category_company['Industry Group'] == '유틸리티'
섹터부동산 = category_company['Industry Group'] == '부동산'

category_company.loc[섹터에너지,'Sector'] = '에너지'
category_company.loc[섹터소재,'Sector'] = '소재'
category_company.loc[섹터자본재,'Sector'] = '산업재'
category_company.loc[섹터상업서비스,'Sector'] = '산업재'
category_company.loc[섹터운송,'Sector'] = '산업재'
category_company.loc[섹터자동차및부품,'Sector'] = '경기소비재'
category_company.loc[섹터내구소비재및의류,'Sector'] = '경기소비재'
category_company.loc[섹터소비자서비스,'Sector'] = '경기소비재'
category_company.loc[섹터미디어,'Sector'] = '경기소비재'
category_company.loc[섹터유통,'Sector'] = '경기소비재'
category_company.loc[섹터음식료및담배,'Sector'] = '필수소비재'
category_company.loc[섹터생활용품,'Sector'] = '필수소비재'
category_company.loc[섹터의료장비및서비스,'Sector'] = '의료'
category_company.loc[섹터제약및바이오,'Sector'] = '의료'
category_company.loc[섹터은행,'Sector'] = '금융'
category_company.loc[섹터보험,'Sector'] = '금융'
category_company.loc[섹터증권,'Sector'] = '금융'
category_company.loc[섹터소프트웨어,'Sector'] = 'IT'
category_company.loc[섹터IT하드웨어,'Sector'] = 'IT'
category_company.loc[섹터반도체,'Sector'] = 'IT'
category_company.loc[섹터디스플레이,'Sector'] = 'IT'
category_company.loc[섹터통신서비스,'Sector'] = '통신서비스'
category_company.loc[섹터유틸리티,'Sector'] = '유틸리티'
category_company.loc[섹터부동산,'Sector'] = '부동산'

