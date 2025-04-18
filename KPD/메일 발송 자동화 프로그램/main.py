# 실행 스크립트
# 0) 사용자 입력
# 1) 데이터 로드(load_requests)
# 2) 필터링(user_name, receive_date 등)
# 3) 메일 생성, 저장, 발송

import sys
import tkinter as tk
from tkinter import simpledialog

import win32com.client as client
import pandas as pd

from config import subject_template, mail_template, attachments, person_path
from reader import load_requests, load_contacts, _copy_to_local

def ask(prompt, title="입력"):
    """tkinter 다이얼로그를 문자열로 입력받습니다."""
    root = tk.Tk()
    root.withdraw() # 메인 윈도우 숨기기
    result = simpledialog.askstring(title, prompt)
    root.destroy()
    if result is None:
        sys.exit("입력이 취소되었습니다.")
    return result.strip()



def main():
    # ── 0) 사용자 입력(GUI 다이얼로그) ────────────────────────────────────────────
    user_name = ask("자료요청 담당자 이름을 입력하세요: ")
    receive_date = ask("자료 회신 요청 일정을 입력하세요 (예: 2025-04-21(월)): ")
    # user_tel = input("자료요청 담당자 전화번호를 입력하세요: ").strip()
    statement_date = ask("재무제표 기준일을 입력하세요 (예: 2025-03-31): ")
    cutoff_monthend = ask("평가기준월말을 입력하세요 (예: 2025년 3월 말): ")
    test_mode_input = ask("테스트 모드로 첫 번째 메일만 작성하시겠습니까? (y/n): ")
    test_mode = test_mode_input.lower() == 'y'

    # ── 0-1) 평가자 연락처 불러오기 ─────────────────────────
    contacts_df = load_contacts()

    # 엑셀에 '이름'과 '전화번호' 컬럼이 있다고 가정
    match = contacts_df.loc[contacts_df['이름'] == user_name]
    if not match.empty:
        user_tel = match.iloc[0]['전화번호']
    else:
        print(f"[!] '{user_name}' 연락처를 평가자연락처.xlsx에서 찾을 수 없습니다.")
        sys.exit(1)


    # ── 1) 엑셀 읽기 및 필터링 ────────────────────────────────────────────
    df = load_requests()
    cond1 = df['재평가/신규'].str.contains('신규', na=False)
    cond2 = df['자료요청담당'].str.contains(user_name, na=False)
    cond3 = df['평가종류코드'].str.contains('B01', na=False) # 펀드 
    df_filtered = df[cond1 & cond2 & cond3]
    
    if df_filtered.empty:
        print(f"[!] '{user_name}' 담당자 조건에 맞는 신규 데이터가 없습니다.")
        sys.exit(1)

    # ── 2) Outlook 연결 ─────────────────
    outlook = client.Dispatch("Outlook.Application")
    rows    = [df_filtered.iloc[0]] if test_mode else df_filtered.to_dict('records')


    # ── 4) 메일 작성 루프 ────────────────
    for row in rows:
        mail = outlook.CreateItem(0)

        # 4-1) 제목
        mail.Subject = subject_template.format(
            기관=row['메인GP 또는 의뢰업체']
        )

        # 4-2) 본문 포맷팅 (Jinja2 로 렌더링 → HTMLBody)
        html_body = mail_template.render(
            담당자                  = row['담당자'],
            기관                    = row['메인GP 또는 의뢰업체'],
            기관명 = row['기관명'],
            종목명 = row['종목명'],
            자료회신요청일정         = receive_date,
            자료요청담당자           = user_name,
            자료요청담당자전화번호   = user_tel,
            재무제표기준일           = statement_date,
            평가기준월말             = cutoff_monthend
        )
        mail.HTMLBody = html_body

        # 4-3) 수신·참조
        mail.To  = row['email']
        mail.CC  = 'npl_2@koreaap.com'

        # 4-4) 첨부파일
        for path in attachments:
            local_attach = _copy_to_local(path)
            mail.Attachments.Add(local_attach)

        # 4-5) 저장/발송/디스플레이
        if test_mode:
            mail.Display()
            print(">> 테스트 모드: 첫 번째 메일 창을 열었습니다.")
            break
        else:
            mail.Save()
            # mail.Send()
            print(f">> Draft 저장: {row['담당자']} <{row['email']}>")

    if test_mode:
        print("테스트가 완료되었습니다. Outlook에서 메일 내용을 확인하세요.")

if __name__ == "__main__":
    main()

