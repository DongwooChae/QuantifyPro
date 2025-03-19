import tkinter as tk
from tkinter import ttk, messagebox
import average_price_module
import pandas as pd

# 프로그램 설정
WINDOW_TITLE = 'Multiple Valuation'
WINDOW_SIZE = '800x600'
FONT_SIZE = 9
FONT = ('맑은 고딕', FONT_SIZE)

# 메인 윈도우 설정
root = tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(WINDOW_SIZE)

# 입력 프레임 (좌측정렬)
input_frame = tk.Frame(root)
input_frame.pack(pady=15, padx=15, anchor='w')

# 평가기준일 입력
tk.Label(input_frame, text='평가기준일 (예:2023-06-30):', font=FONT).grid(row=0, column=0, pady=5, sticky='w')
valuation_date_entry = tk.Entry(input_frame, font=FONT, width=20)
valuation_date_entry.grid(row=0, column=1, pady=5, padx=5)

# 배수시작일 입력
tk.Label(input_frame, text='배수시작일 (예:2023-01-01):', font=FONT).grid(row=1, column=0, pady=5, sticky='w')
start_date_entry = tk.Entry(input_frame, font=FONT, width=20)
start_date_entry.grid(row=1, column=1, pady=5, padx=5)

# 배수종료일 입력
tk.Label(input_frame, text='배수종료일 (예:2023-06-30):', font=FONT).grid(row=2, column=0, pady=5, sticky='w')
end_date_entry = tk.Entry(input_frame, font=FONT, width=20)
end_date_entry.grid(row=2, column=1, pady=5, padx=5)

# 버튼 클릭 시 실행 함수
def calculate():
    valuation_date = valuation_date_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    if not valuation_date or not start_date or not end_date:
        messagebox.showerror('입력 오류', '모든 날짜를 정확히 입력해주세요.')
        return

    try:
        result_df = average_price_module.calculate_valuation(
            valuation_date, start_date, end_date)

        # 출력할 열 한정 및 반올림 처리
        cols_to_show = ['EPS', 'BPS', 'SPS', '평균주가', 'PER', 'PBR', 'PSR']
        result_df = result_df[cols_to_show].round(2)

        # 표 초기화
        for item in tree.get_children():
            tree.delete(item)

        # 컬럼 설정 (인덱스 포함)
        tree["columns"] = ['종목명'] + cols_to_show
        tree["show"] = "headings"

        tree.heading('종목명', text='종목명')
        tree.column('종목명', anchor='center', width=120)

        for col in cols_to_show:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=100)

        # 데이터 삽입 (인덱스 포함)
        for idx, row in result_df.iterrows():
            tree.insert("", "end", values=[idx] + row.tolist())

    except Exception as e:
        messagebox.showerror('오류', str(e))

# 계산하기 버튼 (우측 위치)
calc_button = tk.Button(input_frame, text='계산하기', command=calculate, font=FONT, width=15)
calc_button.grid(row=2, column=2, padx=20)

# 결과 표시 영역 (데이터프레임 표 형식으로)
tree_frame = tk.Frame(root)
tree_frame.pack(fill='both', expand=True, padx=15, pady=10)

tree_scroll_y = tk.Scrollbar(tree_frame, orient='vertical')
tree_scroll_x = tk.Scrollbar(tree_frame, orient='horizontal')

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

tree_scroll_y.pack(side='right', fill='y')
tree_scroll_x.pack(side='bottom', fill='x')

tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)

tree.pack(fill='both', expand=True)

# 메인 루프
root.mainloop()