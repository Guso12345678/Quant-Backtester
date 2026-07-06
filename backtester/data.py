import yfinance as yf 
import pandas as pd

def load_data(ticker:str, start:str, end:str)->pd.DataFrame: 
    df = yf.download(ticker,start,end,progress=False)
    if df.empty: 
        raise ValueError(f"No se encontraron datos para {ticker} entre {start} y {end}")
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0) #Because the yfinance, return the data with MultiIndex columns, and after for computing the means in the strategy of SMA will raise an error. 
    df = df[["Open","High","Low","Close","Volume"]]
    df = df.sort_index()
    df = df.dropna()#Avoid using NaN for any comparison or calculations. 

    return df 

def load_df(path:str): 
    df = pd.read_csv(filepath_or_buffer=path,parse_dates=["Date"],index_col=["Date"])
    df = df.sort_index()
    df = df.dropna()
    return df
