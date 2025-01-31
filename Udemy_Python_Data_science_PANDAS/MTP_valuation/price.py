import pandas as pd
import numpy as np
import xlwings as xw

# Backdata(Dataframe)
# financial_data_path = r"C:\Users\User\Udemy_Python_Data_science_PANDAS\MTP_valuation\241Q재무데이터.csv"
# stock_count_path = r"C:\Users\User\Udemy_Python_Data_science_PANDAS\MTP_valuation\241Q주식수.csv"
# main_products_path = r"C:\Users\User\Udemy_Python_Data_science_PANDAS\MTP_valuation\주요상품.csv"

pricedata_path = r"C:\Users\User\Udemy_Python_Data_science_PANDAS\MTP_valuation\수정주가.csv"
pricedata = pd.read_csv(pricedata_path, index_col="company")


pricedata.head()