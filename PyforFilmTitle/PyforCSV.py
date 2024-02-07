import pandas as pd
from pandas import DataFrame
import requests
import time
import os

# 打印当前工作目录
print(os.getcwd())

# data = pd.read_excel('00_15.xlsx')
# data = data[:15]
# data.to_csv('00_15.csv', index=False, encoding='utf-8')

data = pd.read_excel('16_30.xlsx')
data = data[15:30]
data.to_csv('16_30.csv', index=False, encoding='utf-8')

data = pd.read_excel('31_50.xlsx')
data = data[30:]
data.to_csv('31_50.csv', index=False, encoding='utf-8')

