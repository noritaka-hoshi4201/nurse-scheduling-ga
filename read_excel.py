import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), './lib'))

import pandas as pd
import datetime

# setup
# pip install pandas -t ./lib --upgrade
# pip install openpyxl -t ./lib --upgrade
# pip install xlrd -t ./lib --upgrade




if __name__ == '__main__':
    """https://note.nkmk.me/python-pandas-read-excel/
    """    
    df = pd.read_excel('data/item.xlsx', index_col=0)
    print(f"{df}")
    print(f"dimention: {df.shape[0]} - {df.shape[1]}")
    print(f"dimention2: {len(df)} - {len(df.columns)}")
    print(f"index: {df.index} - {len(df.index)}")
    print(f"columns: {df.columns}")
