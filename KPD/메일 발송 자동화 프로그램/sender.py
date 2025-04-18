# Outlook COM 연결, 메일 생성 및 발송 함수

message = outlook.CreateItem(0)

message.To = 'test@test.com' # 수신
message.CC = 'test@test.com' # 참조
message.BCC = 'test@test.com' # 숨은참조
message.Subject = 'Title' # 메일 제목
message.body  = 'Content' # 메일 본문
message.Save() # 보낼편지함(Draft)폴더에 메시지를 저장 # message.Send()로 바꾸면 메시지가 발송됨

for i, r in df.iterrows():
    message = outlook.Createitem(0)
    message.To = r['E-Mail']
    message.Subject = "[KAP] 비시장성지분증권 공정가치 평가관련 자료요청의 건({GP}})"
    message.body = f"안녕하십니까? 한국자산평가입니다.
당사는 2025년 반기부터 산은캐피탈의 공정가치 평가를 수행하게 되었음을 알려드리며, 이를 원활히 진행하기 위해 산은캐피탈 측과 협의한 결과, 첨부와 같이 2025년 3월 31일 기준 펀드재무제표 및 2024년 12월 31일 기준 기초자산 평가 관련 자료를 사전에 요청드리고자 합니다.
또한, 사전 자료 회신 이후에는 2025년 6월 30일 기준 본 평가 시점에 맞추어, 2025년 5월 31일 기준 펀드 재무제표 및 투자자산의 변동내역 또는 자본변동내역 등을 별도로 재요청드릴 예정이오니, 번거로우시겠지만, 하기 일정까지 자료를 회신해 주시면 감사하겠습니다.

자료 회신 요청 일정: {자료회신요청일정}
문의사항이 있으시다면 언제든 연락 주시기 바랍니다.

{자료요청담당자} 드림({자료요청담당자전화번호})
"