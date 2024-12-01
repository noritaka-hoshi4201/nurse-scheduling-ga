# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), './lib'))

import random
from scoop import futures

from deap import base
from deap import creator
from deap import tools
from deap import cma

import data_set


class Schedule(object):
    src_data = None
    def __init__(self, list_shift=None):
        # print(f"__init__ {list_shift}")
        if self.__class__.src_data is None:
            self.__class__.src_data = data_set.ItemData()
        self._data = self.__class__.src_data
        self._list_sale_item = self._data.data_list
        self._list_shift = self.make_sample(self._data.data_set_count) if list_shift is None else list_shift

    def save(self) -> str:
        return self.__class__.src_data.save(self.slice_item_shift())

    @property
    def len_item(self) -> int:
        return self._data.item_count

    @property
    def len_shift(self) -> int:
        return self._data.data_count

    @property
    def len_item_shift_all(self) -> float:
        return float(self._data.data_set_count)

    # ランダムなデータを生成
    @classmethod
    def make_sample(cls, total) -> list:
        print(f"make_sample: {total}")
        sample_list = []
        for _num in range(total):
            sample_list.append(random.randint(0, 1))
        return sample_list

    # タプルを1ユーザ単位に分割
    def slice_item_shift(self) ->tuple:
        sliced = []
        try:
            for index in range(self.len_item):
                offset = index*self.len_shift
                sliced.append(self._list_shift[offset:(offset + self.len_shift)])
            return tuple(sliced)
        except Exception as ex:
            print(f"slice_item_shift error: {ex}")
            raise ex

    # CSV形式でアサイン結果の出力をする
    def print_csv(self):
        shifts = self.slice_item_shift()

        print("jan,will," + ",".join(data_set.KEY_WEEK))
        for index in range(len(shifts)):
            item = self._list_sale_item[index]
            print( f"{item.jan},{item.will}," + ','.join(map(str, shifts[index])))

    # TSV形式でアサイン結果の出力をする
    def print_tsv(self):
        for line in self.slice_item_shift():
            print(f"{line}")
            print("\t".join(map(str, line)))

    # ユーザ番号を指定してコマ名を取得する
    def get_boxes_by_user(self, user_no):
        line = self.slice_item_shift()[user_no]
        return self.line_to_box(line)

    # 1ユーザ分のタプルからコマ名を取得する
    def line_to_box(self, line):
        result = []
        index = 0
        for e in line:
            if e == 1:
                result.append(data_set.KEY_WEEK[index])
            index = index + 1
        return result

    # アサインが応募コマ数の50%に満たないユーザを取得
    def few_work_user(self):
        result = []
        for user_no in range(10):
            item = self._list_sale_item[user_no]
            ratio = float(len(self.get_boxes_by_user(user_no))) / float(item.will)
            if ratio < 0.5:
                result.append(item)
        return result

    # 想定人数と実際の人数の差分を取得する
    def abs_item_between_need_and_actual(self):
        result = []
        index = 0
        for need in self._data.need_list:
            actual = len(self.get_item_nos_by_box_index(index))
            result.append(abs(need - actual))
            index += 1
        return result
    
    # コマ番号を指定してアサインされているユーザ番号リストを取得する
    def get_item_nos_by_box_index(self, box_index):
        user_nos = []
        index = 0
        for line in self.slice_item_shift():
            # print(f"{line} - {box_index}")
            if line[box_index] == 1:
                user_nos.append(index)
            index += 1
        return user_nos