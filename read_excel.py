import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), './lib'))

import pandas as pd
import datetime

# setup
# pip install pandas -t ./lib --upgrade
# pip install openpyxl -t ./lib --upgrade
# pip install xlrd -t ./lib --upgrade

def read_excel() -> dict:
    path = os.path.join(os.path.dirname(__file__),"data/item.xlsx")
    df = pd.read_excel(path, index_col=0)
    print(f"{df}")
    print(f"dimention: {df.shape[0]} - {df.shape[1]}")
    print(f"dimention2: {len(df)} - {len(df.columns)}")
    print(f"index: {df.index} - {len(df.index)}")
    print(f"{list(df.index)}")
    print(f"columns: {df.columns}")



if __name__ == '__main__':
    """https://note.nkmk.me/python-pandas-read-excel/
    """
    read_excel()

    sample = [1,2,3,4] 
    
    tmp = sample + [sum(sample)]
    print(tmp)

