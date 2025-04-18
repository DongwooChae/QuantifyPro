import os, sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

# 1) 번들 내부 혹은 소스 폴더의 template 디렉터리 경로
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)
template_dir = os.path.join(base_path, 'templates')



# 1) templates_dir (번들 내부 또는 소스 폴더의 templates)를 로더에 지정
template_env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml'])
)

# 2) mail_body.html 템플릿 로드
mail_template = template_env.get_template('mail_body.html')

# 3) 제목 템플릿 (Jinja2 변수 표현식 {{ 기관 }})
subject_template = "[KAP] 비시장성지분증권 공정가치 평가관련 자료요청의 건 ({기관})"

# 4) 요청 리스트가 담긴 엑셀 파일 경로
excel_path = r"\\10.10.10.11\Ai본부\F.AI본부\@대체평가2사업본부\메일 발송 자동화 프로그램\운용사(사전)자료요청담당자정리_2025년2분기_산은캐피탈_GP수정본_250416.xlsx"
# excel_path = r"C:\Users\dwchae23\Desktop\일정관리\의뢰리스트 확정 및 자료요청 일괄 전송메일\25.2Q\운용사(사전)자료요청담당자정리_2025년2분기_산은캐피탈_GP수정본_250416.xlsx"

# 5) 첨부파일 리스트
attachments = [r"\\10.10.10.11\Ai본부\F.AI본부\@대체평가2사업본부\메일 발송 자동화 프로그램\산은캐피탈_펀드요청자료목록_20250331(사전요청).xlsx"]
# attachments = [r"C:\Users\dwchae23\Desktop\일정관리\의뢰리스트 확정 및 자료요청 일괄 전송메일\25.2Q\산은캐피탈_펀드요청자료목록_20250331(사전요청).xlsx"]

# 6) 평가자 연락처 파일 경로
person_path = r"\\10.10.10.11\Ai본부\F.AI본부\@대체평가2사업본부\메일 발송 자동화 프로그램\평가자연락처.xlsx"
# person_path = r"C:\Users\dwchae23\Desktop\일정관리\의뢰리스트 확정 및 자료요청 일괄 전송메일\25.2Q\평가자연락처.xlsx"

# 4) 메일 본문 템플릿 (프로그램 안에서 직접 수정·관리)
#    Jinja2 없이 str.format 혹은 간단한 replace 로도 활용할 수 있습니다.
