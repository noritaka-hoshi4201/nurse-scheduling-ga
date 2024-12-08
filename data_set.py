"""  """
import os
import shutil
from datetime import datetime

from sale_item import SaleItem
import pandas as pd


HEADER_CNT = 3 # 先頭3+1行読み飛ばし
HEADER_WILL = 2 # 発注希望数行のindex

HEADER_PARAM_CNT = 2 # param の開始行
IDX_PARAM_TOTAL_COUNT = 0 # 全体の希望数
IDX_PARAM_PRIORITY = 1    # 商品の優先度
IDX_PARAM_TYPES = 2       # 商品の種類数
IDX_PARAM_CONTINUOUS = 3  # 商品の連続数

# 評価関数の種類数
# EVAL_PARAM_COUNT = 4
EVAL_PARAM_COUNT = 3

KEY_NAME = "name"
KEY_PRI = "priority"
KEY_WILL = "will"

KEY_WEEK = ["mon","tue","wed","thu","fri","sat","sun"]
KEY_TOTAL = "total"
KEY_ORDERPTN2 = "orderptn2"

SRC_PATH = os.path.join(os.path.dirname(__file__),"data/item.xlsx")

class ItemData(object):
    """_summary_

    Args:
        Object (_type_): _description_
    """
    _eval_count = 0

    def __init__(self):
        """_summary_
        """
        path = SRC_PATH
        df = pd.read_excel(path, index_col=0)
        self.load_data(df)
        self.load_param(df)
        print(f"get_calc_param: {self.get_calc_param()}")

    def load_data(self, df):
        """データロード

        Args:
            df (_type_): _description_

        Raises:
            ValueError: _description_
        """        
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

            lst2 = list(df.index.unique())
            for idx, val in enumerate(lst2):
                if val == 'JAN':
                    lst2 = lst2[(idx+1):]
                    break
            if len(lst) != len(lst2):
                print(f"lst: {lst}" )
                print(f"lst2: {lst2}" )
                raise ValueError("JAN に重複が存在します")


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

    def load_param(self, df):
        """パラメータの取得

        Args:
            df (_type_): _description_
        """        
        header = list(df.columns)
        param_index = header.index("param")

        # 計算パラメータ
        offset = 0
        self._pop = int(df.iat[HEADER_PARAM_CNT+offset, param_index])
        offset += 1
        self._cxpb = float(df.iat[HEADER_PARAM_CNT+offset, param_index])
        offset += 1
        self._mutpb = float(df.iat[HEADER_PARAM_CNT+offset, param_index])
        offset += 1
        self._ngen  = int(df.iat[HEADER_PARAM_CNT+offset, param_index])

        # 評価パラメータ
        self._eval_params =[]

        for _idx in range(EVAL_PARAM_COUNT):
            offset += 3
            sub1 = df.iat[HEADER_PARAM_CNT+offset, param_index+1]
            if len(str(sub1)) == 0:
                sub1 = 0 
            sub2 = df.iat[HEADER_PARAM_CNT+offset, param_index+2]
            if len(str(sub2)) == 0:
                sub2 = 0 
            self._eval_params.append([
                int(df.iat[HEADER_PARAM_CNT+offset, param_index]),
                sub1,
                sub2])

    def get_calc_param(self) -> tuple:
       return self._pop, self._cxpb, self._mutpb, self._ngen

    def get_eval_fitness(self) -> tuple:
        """各評価の重要度付き評価方法を返す
        Returns:
            tuple: _description_
        """
        lst = []
        for param in self._eval_params:
            lst.append(param[0])
        print(f"get_eval_fitness: {lst}")
        return tuple(lst)

    @property
    def eval_count(self) -> int:
        return self.__class__._eval_count

    def get_eval_value(self, lst_data: list) -> tuple:
        """評価関数

        Args:
            lst_data (list): _description_

        Returns:
            tuple: _description_
        """
        self.__class__._eval_count += 1

        week_total = [0,0,0,0,0,0,0]
        item_score_total = 0

        # ２個目以降の減衰値
        param_pri = self._eval_params[IDX_PARAM_PRIORITY]
        # 優先度の減少値
        pri_dec_under = param_pri[1] # 希望数以下の時
        pri_dec_over = param_pri[2] # 希望数超えた時

        item_index = 0
        types_cnt = 0
        while item_index < len(lst_data):
            item = self.data_list[item_index]
            schedule = lst_data[item_index]
            cnt = sum(schedule)
            will = item.will
            pri_current = item.priority

            if cnt > 0:
                # 商品種類数
                types_cnt +=1

            #優先度の評価
            diff = (cnt-will)
            if diff > 0:
                # 希望数より多い
                item_score_total += diff*diff*pri_current/pri_dec_over
            elif diff < 0:
                tmp = diff*diff*pri_current/pri_dec_under
                item_score_total += tmp
            
            for wday in range(7):
                week_total[wday] += schedule[wday]
            item_index +=1

        # ２個目以降の減衰値
        param_total = self._eval_params[IDX_PARAM_TOTAL_COUNT]
        # 優先度の減少値
        total_dec_under = param_total[1] # 希望数以下の時
        total_dec_over = param_total[2] # 希望数超えた時

        # print(f"week_total: {week_total}")
        count_score_total = 0
        for idx, will in enumerate(self._need):
            tmp = week_total[idx] - will
            if will > week_total[idx]:
                # 不足分カウント
                count_score_total += tmp*tmp*total_dec_under
            else:
                # 過剰分カウント
                count_score_total += tmp*tmp*total_dec_over
        # ret = (count_score_total, item_score_total, types_cnt, continuous_total)
        ret = (count_score_total, item_score_total, types_cnt)
        # print(f"eval: {ret}")
        return ret


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

        wday_total = [0,0,0,0,0,0,0]

        for key in index:
            tmp = lst[offset]
            odnp = f"d{tmp[0]}{tmp[1]}{tmp[2]}{tmp[3]}{tmp[4]}{tmp[5]}{tmp[6]}"
            odnp2 = f"D{tmp[6]}{tmp[0]}{tmp[1]}{tmp[2]}{tmp[3]}{tmp[4]}{tmp[5]}"
            tmp = tmp + [sum(lst[offset])] + [odnp,odnp2]
            df.loc[key, KEY_WEEK[0]:KEY_ORDERPTN2] = tmp

            wday_total = [ val1+val2 for val1, val2 in zip(wday_total, tmp)]
            offset += 1

        # 曜日毎の総計
        wday_total = wday_total + [sum(wday_total)]
        df.loc[list(df.index)[1],KEY_WEEK[0]:KEY_TOTAL] = wday_total
        # print(f"wday_total: {list(df.index)[1]} -> {wday_total}")

        evals = self.get_eval_value(lst)
        header = list(df.columns)
        param_index = header.index("param")

        offset = 6
        for eval in evals:
            df.iat[HEADER_PARAM_CNT+offset, param_index+3] = eval
            offset += 3

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
    

