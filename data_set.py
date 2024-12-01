"""  """
import os
import shutil
from datetime import datetime

from sale_item import SaleItem
import pandas as pd


HEADER_CNT = 3 # 先頭3+1行読み飛ばし
HEADER_WILL = 2 # 発注希望数行のindex
KEY_NAME = "name"
KEY_PRI = "priority"
KEY_WILL = "will"

KEY_WEEK = ["mon","tue","wed","thu","fri","sat","sun"]
KEY_TOTAL = "total"

SRC_PATH = os.path.join(os.path.dirname(__file__),"data/item.xlsx")

class ItemData(object):
    """_summary_

    Args:
        Object (_type_): _description_
    """

    def __init__(self):
        """_summary_
        """
        path = SRC_PATH
        df = pd.read_excel(path, index_col=0)
        items = []
        need = []
        while True:
          lst = list(df.index)
          if len(lst) <= HEADER_CNT:
              break

          key = lst[HEADER_WILL]
          for item in KEY_WEEK:
              need.append(int(df.at[key, item]))

          lst = lst[HEADER_CNT:]
          for jan in lst:
              items.append(SaleItem(
                  jan=jan,
                  name=df.at[jan, KEY_NAME],
                  pri=df.at[jan, KEY_PRI],
                  will=df.at[jan, KEY_WILL]
              ))
          break
        self._need = need
        self._items = items

    def save(self, lst:list)->str:
        """_summary_

        Args:
            lst (list): _description_

        Returns:
            str: _description_
        """
        dir = os.path.dirname(SRC_PATH)
        fname = os.path.basename(SRC_PATH).split(".")[0] + datetime.now().strftime("-%Y%m%d-%H%M%S.xlsx")
        path = os.path.join(dir, fname)
        shutil.copy(SRC_PATH, path)
        df = pd.read_excel(path, index_col=0)
        index = list(df.index)
        index = index[HEADER_CNT:]
        offset = 0
        for key in index:
          tmp = lst[offset] + [sum(lst[offset])]
          df.loc[key, KEY_WEEK[0]:KEY_TOTAL] = tmp
          offset += 1
        with pd.ExcelWriter(path, 
                            engine="openpyxl", 
                            mode="a", 
                            if_sheet_exists="overlay") as writer:
            df.to_excel(writer)
        return path


    @property
    def data_list(self) -> list:
      return self._items

    @property
    def item_count(self) -> int:
      return len(self._items)

    @property
    def data_count(self) -> int:
      return len(KEY_WEEK)

    @property
    def data_set_count(self) -> int:
      return len(self._items)*len(KEY_WEEK)

    @property
    def need_list(self) -> list:
      return self._need
    

