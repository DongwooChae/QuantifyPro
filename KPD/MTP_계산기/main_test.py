import tkinter as tk
from tkinter import ttk, messagebox
import average_price_module
import pandas as pd

# 설정
FONT = ('맑은 고딕', 9)
root = tk.Tk()
root.title('Multiple_valuation_TEST')
root.geometry('1200x700')

current_df = pd.DataFrame()

# 입력 프레임
input_frame = tk.Frame(root)
input_frame.pack(side='top', fill='x', padx=10, pady=10, anchor='w')

# 입력 필드
labels = ['평가기준일:', '배수시작일:', '배수종료일:', '개별기업 검색:']
entries = []
for idx, label in enumerate(labels):
    tk.Label(input_frame, text=label, font=FONT).grid(row=0, column=idx*2, padx=5, sticky='w')
    entry = tk.Entry(input_frame, font=FONT, width=15)
    entry.grid(row=0, column=idx*2+1, padx=5)
    entries.append(entry)

# 계산하기 버튼
def calculate():
    global current_df
    valuation_date, start_date, end_date = entries[0].get(), entries[1].get(), entries[2].get()
    try:
        current_df = average_price_module.calculate_valuation(valuation_date, start_date, end_date)
        current_df = current_df[['EPS','BPS','SPS','평균주가','PER','PBR','PSR']].round(2)
        update_tree(tree_left, current_df)
    except Exception as e:
        messagebox.showerror("오류", str(e))

calc_button = tk.Button(input_frame, text='계산하기', command=calculate, font=FONT, width=12)
calc_button.grid(row=0, column=6, padx=10)

# 검색 기능 (Enter 지원)
def search_company(event=None):
    query = entries[3].get().lower()
    if current_df.empty or not query:
        return
    filtered_df = current_df[current_df.index.str.lower().str.contains(query)]
    update_tree(tree_left, filtered_df)

entries[3].bind('<Return>', search_company)

search_button = tk.Button(input_frame, text='검색하기', command=search_company, font=FONT, width=12)
search_button.grid(row=0, column=7, padx=(20,5))  # 20px 간격 조정

# 전체리스트 버튼
def show_all():
    update_tree(tree_left, current_df)

all_button = tk.Button(input_frame, text='전체 리스트', command=show_all, font=FONT, width=12)
all_button.grid(row=0, column=8, padx=5)

# 좌우 프레임 (비율 6:4)
left_frame = tk.Frame(root)
left_frame.place(relx=0, rely=0.1, relwidth=0.6, relheight=0.9)

right_frame = tk.Frame(root)
right_frame.place(relx=0.6, rely=0.1, relwidth=0.4, relheight=0.9)

# 좌측 트리뷰
tree_left = ttk.Treeview(left_frame)
tree_left.pack(fill='both', expand=True)

# 우측 트리뷰 (체크박스 포함)
columns_right = ['종목명','PER','PBR','PSR','포함']
tree_right = ttk.Treeview(right_frame, columns=columns_right, show='headings')
for col in columns_right:
    tree_right.heading(col, text=col)
    tree_right.column(col, anchor='center', width=80)
tree_right.pack(fill='both', expand=True)

# 체크박스 관리
checkboxes = {}

def add_to_right(event):
    item = tree_left.selection()
    if item:
        values = tree_left.item(item[0])['values']
        selected = [values[0], values[5], values[6], values[7], '']
        iid = tree_right.insert("", "end", values=selected)
        
        var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(tree_right, variable=var, width=0)
        tree_right.set(iid, column='포함', value='')
        tree_right.update_idletasks()
        
        x, y, width, height = tree_right.bbox(iid, column='포함')
        chk_window = tree_right.master.create_window(x+width//2, y+height//2, window=chk)
        checkboxes[iid] = var

tree_left.bind('<Double-1>', add_to_right)

# 트리뷰 업데이트 함수
def update_tree(tree, df):
    tree.delete(*tree.get_children())
    cols = ['종목명'] + list(df.columns)
    tree["columns"] = cols
    tree["show"] = "headings"
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=90)
    for idx, row in df.iterrows():
        formatted_row = [f"{v:,.2f}" if isinstance(v, float) else v for v in row]
        tree.insert("", "end", values=[idx] + formatted_row)

# 가치배수 평균 계산 및 초기화
def calculate_average():
    rows = []
    for iid, var in checkboxes.items():
        if var.get():
            values = tree_right.item(iid)['values'][1:4]
            rows.append([float(v.replace(',','')) for v in values])
    if rows:
        df = pd.DataFrame(rows, columns=['PER','PBR','PSR'])
        mean_vals = df.mean().round(2)
        avg_result.delete(*avg_result.get_children())
        avg_result.insert("", "end", values=[f"{mean_vals[col]:,.2f}" for col in mean_vals.index])

def reset_average():
    avg_result.delete(*avg_result.get_children())

# 리셋 버튼 (우측상단)
def reset_right_tree():
    tree_right.delete(*tree_right.get_children())
    global checkboxes
    checkboxes = {}
    reset_average()

reset_button_top = tk.Button(right_frame, text='리셋', command=reset_right_tree, font=FONT, width=10)
reset_button_top.pack(pady=3)

# 가치배수 평균값 계산 버튼과 초기화 버튼
avg_button_frame = tk.Frame(right_frame)
avg_button_frame.pack(pady=5)

avg_button = tk.Button(avg_button_frame, text='가치배수 평균값 계산', command=calculate_average, font=FONT, width=20)
avg_button.pack(side='left', padx=5)

reset_button = tk.Button(avg_button_frame, text='초기화', command=reset_average, font=FONT, width=10)
reset_button.pack(side='left', padx=5)

# 평균값 결과 표시
avg_result = ttk.Treeview(right_frame, columns=['PER','PBR','PSR'], show='headings', height=2)
for col in ['PER','PBR','PSR']:
    avg_result.heading(col, text=col)
    avg_result.column(col, anchor='center', width=80)
avg_result.pack(fill='x', pady=5)

root.mainloop()
