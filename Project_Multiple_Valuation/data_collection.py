import os
import pandas as pd
import yfinance as yf

# TICKER 폴더 경로 설정 (예: 섹터별 CSV 파일이 있는 폴더)
ticker_folder_path = 'C:/Users/dwchae23/QuantifyPro/workplace/Project_Multiple_Valuation/TICKER'

# 주요 칼럼 리스트
selected_columns = [
    'symbol', 'shortName', 'sector', 'industry', 'country', 'beta',
    'trailingPE', 'forwardPE', 'priceToBook', 'enterpriseToRevenue', 'enterpriseToEbitda',
    'trailingPegRatio', 'marketCap', 'enterpriseValue', 'profitMargins', 'sharesOutstanding',
    'bookValue', 'grossMargins', 'ebitdaMargins', 'operatingMargins', 'revenuePerShare',
    'returnOnAssets', 'returnOnEquity', 'ebitda', 'totalDebt', 'totalRevenue', 'payoutRatio',
    'trailingEps', 'forwardEps', 'pegRatio', 'debtToEquity', 'freeCashflow', 'operatingCashflow',
    'earningsGrowth', 'revenueGrowth', 'longBusinessSummary'
]

# 재무 데이터를 수집하는 함수
def fetch_financial_data_by_ticker(ticker):
    """
    특정 티커에 대한 재무 데이터를 수집하고, 주요 컬럼만 반환합니다.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return {col: info.get(col, 'N/A') for col in selected_columns}

# 피클 파일로 데이터프레임 저장
def save_dataframe_to_pickle(df, filename):
    df.to_pickle(filename)
    print(f"DataFrame saved to {filename}")

# 섹터별 파일을 순차적으로 처리
def process_sector_files(ticker_folder_path):
    # 폴더 내의 모든 파일을 순회
    for file_name in os.listdir(ticker_folder_path):
        if file_name.endswith('.csv'):
            sector_name = os.path.splitext(file_name)[0]
            sector_file_path = os.path.join(ticker_folder_path, file_name)
            
            # 섹터별 CSV 파일에서 티커 목록 불러오기
            df_tickers = pd.read_csv(sector_file_path)
            tickers = df_tickers['Symbol'].dropna().tolist()  # 'Symbol' 열을 사용한다고 가정

            # 모든 티커에 대한 재무 데이터를 수집
            financial_data = []
            for ticker in tickers:
                data = fetch_financial_data_by_ticker(ticker)
                financial_data.append(data)

            # 수집된 데이터를 데이터프레임으로 변환
            sector_info_df = pd.DataFrame(financial_data)

            # 섹터별로 데이터프레임을 피클 파일로 저장
            pickle_filename = f"{sector_name}_info_df.pkl"
            save_dataframe_to_pickle(sector_info_df, pickle_filename)

if __name__ == "__main__":
    # 섹터별 파일 처리 시작
    process_sector_files(ticker_folder_path)
