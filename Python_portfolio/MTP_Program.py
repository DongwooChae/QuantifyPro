import pandas as pd
import tkinter as tk
from tkinter import ttk

# 데이터셋 준비 (미리 로드된 CSV 파일)
file_path = r'C:\Users\dwchae23\QuantifyPro\workplace\Python_portfolio\sector\healthcare.csv'
data = pd.read_csv(file_path)

# 데이터 내 주요 섹터 목록 (미리 정의된 섹터 리스트)
sectors = [
    "Technology", "Telecommunications", "Healthcare", "Financials", 
    "Real Estate", "Consumer Discretionary", "Consumer Staples", 
    "Industrials", "Basic Materials", "Energy", "Utilities"
]

# Tkinter GUI 설계 시작
root = tk.Tk()
root.title("Project Multiple Valuation")
root.geometry("1200x700")  # 창 크기 조정

# 레이아웃 프레임 설정 (좌측과 우측)
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame, width=200)  # 좌측 프레임 (Sector 체크박스)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

right_frame = tk.Frame(main_frame)  # 우측 프레임 (데이터 디스플레이)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# 체크박스 선택 섹터 저장 리스트
selected_sectors = []

# 섹터 선택 체크박스 UI (좌측 정렬)
sector_label = tk.Label(left_frame, text="Select Sectors:")
sector_label.pack(anchor=tk.W)

sector_vars = {}
for idx, sector in enumerate(sectors):
    var = tk.BooleanVar()
    chk = tk.Checkbutton(left_frame, text=sector, variable=var)
    chk.pack(anchor=tk.W)
    sector_vars[sector] = var

# 테이블 프레임 생성 (우측 프레임 내에)
table_frame = tk.Frame(right_frame)
table_frame.pack(fill=tk.BOTH, expand=True)

# 가로 및 세로 스크롤바 추가
x_scroll = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

y_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# 테이블을 출력하기 위한 Treeview (검색 결과 또는 섹터 결과)
tree = ttk.Treeview(table_frame, columns=list(data.columns), show="headings", height=15, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

# 스크롤바 Treeview에 연결
x_scroll.config(command=tree.xview)
y_scroll.config(command=tree.yview)

# 각 열 크기 기본 설정 (칼럼 크기 조정 문제 해결)
for col in list(data.columns):
    tree.heading(col, text=col, command=lambda c=col: sort_column(c, False))  # 정렬 기능 추가
    tree.column(col, width=150, stretch=True)  # 기본 열 폭 설정

tree.pack(fill=tk.BOTH, expand=True)

# 기업 선택을 위한 체크박스 추가
company_check_vars = {}

def update_company_checkboxes(filtered_data):
    global company_check_vars
    company_check_vars.clear()
    
    # 체크박스가 있는 Treeview를 위해 Row를 하나씩 삭제 후 재추가
    for row in tree.get_children():
        tree.delete(row)
    
    # 체크박스 추가 및 데이터 삽입
    for index, row in filtered_data.iterrows():
        var = tk.BooleanVar()
        company_check_vars[index] = var
        values = list(row)
        tree.insert("", "end", values=values, tags=(str(index),))
        tree.tag_bind(str(index), "<Button-1>", lambda event, index=index: select_company(index))
    
def select_company(index):
    selected = company_check_vars.get(index).get()
    company_check_vars[index].set(not selected)

# 선택된 기업 데이터 취합 및 표시하는 함수
def show_selected_companies():
    selected_data = []
    
    # 선택된 기업만 추출
    for index, var in company_check_vars.items():
        if var.get():
            selected_data.append(data.iloc[index][['Name', 'Book Value', 'Beta', 'Revenue per Share']])
    
    # 선택된 기업 데이터 출력 (우측 하단 디스플레이)
    display_frame = tk.Frame(right_frame)
    display_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    
    for widget in display_frame.winfo_children():
        widget.destroy()  # 이전 내용 삭제
    
    if selected_data:
        df_selected = pd.DataFrame(selected_data)
        # Treeview로 출력
        selected_tree = ttk.Treeview(display_frame, columns=list(df_selected.columns), show="headings", height=5)
        for col in df_selected.columns:
            selected_tree.heading(col, text=col)
            selected_tree.column(col, width=150)
        selected_tree.pack(fill=tk.BOTH, expand=True)
        
        # 데이터 삽입
        for _, row in df_selected.iterrows():
            selected_tree.insert("", "end", values=list(row))
    else:
        no_data_label = tk.Label(display_frame, text="No companies selected.")
        no_data_label.pack()

# 검색 결과를 위한 프레임
search_frame = tk.Frame(right_frame)
search_frame.pack(pady=10)

# 검색창 UI
search_label = tk.Label(search_frame, text="Search by Company Name or Ticker:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT)

# 검색 결과 표시 함수
def search_company():
    search_term = search_entry.get().lower()
    filtered_data = data[
        data['Name'].str.lower().str.contains(search_term) | 
        data['Ticker'].str.lower().str.contains(search_term)
    ]
    update_company_checkboxes(filtered_data)

# 검색 버튼
search_button = tk.Button(search_frame, text="Search", command=search_company)
search_button.pack(side=tk.LEFT)

# 선택한 섹터에 맞는 데이터를 표시하는 함수
def filter_by_sector():
    selected_sectors.clear()
    for sector, var in sector_vars.items():
        if var.get():
            selected_sectors.append(sector)
    
    if selected_sectors:
        filtered_data = data[data['Sector'].isin(selected_sectors)]
        update_company_checkboxes(filtered_data)

# 필터링 버튼
filter_button = tk.Button(left_frame, text="Apply Sector Filter", command=filter_by_sector)
filter_button.pack(pady=5)

# 선택한 기업 리스트를 표시하는 버튼
show_selected_button = tk.Button(left_frame, text="Show Selected Companies", command=show_selected_companies)
show_selected_button.pack(pady=5)

# 컬럼 클릭 시 정렬 기능
def sort_column(col, reverse):
    # 데이터 정렬
    sorted_data = data.sort_values(by=[col], ascending=not reverse)
    update_company_checkboxes(sorted_data)
    
    # 다음 클릭에 대해 반대 정렬로 설정
    tree.heading(col, text=col, command=lambda: sort_column(col, not reverse))

root.mainloop()
