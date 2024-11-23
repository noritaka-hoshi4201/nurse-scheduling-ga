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


# シフトを表すクラス
# 内部的には 3(朝昼晩) * 7日 * 10人 = 210次元のタプルで構成される
class Schedule(object):

  def __init__(self, list_shift):
    self.list_sale_item = data_set.get_data_set()
    self.list_shift = self.make_sample(
      self.len_item_shift_all) if list_shift is None else list_shift

  @property
  def len_item(self) -> int:
    return len(self.list_sale_item)

  @property
  def len_shift(self) -> int:
    return data_set.LEN_SHIFT

  @property
  def len_item_shift_all(self) -> int:
    return data_set.LEN_SHIFT*len(self.list_sale_item)

  # ランダムなデータを生成
  @classmethod
  def make_sample(cls, total) -> list:
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
        sliced.append(self.list_shift[offset:(offset + self.len_shift)])
      return tuple(sliced)
    except Exception as ex:
      print(f"slice_item_shift error: {ex}")
      raise ex


  # ユーザ別にアサインコマ名を出力する
  def print_inspect(self):
    user_no = 0
    for line in self.slice_item_shift():
      print(f"ユーザ{user_no}")
      print(line)
      user_no = user_no + 1

      index = 0
      for e in line:
        if e == 1:
          print(data_set.SHIFT_BOXES[index])
        index = index + 1

  # CSV形式でアサイン結果の出力をする
  def print_csv(self):
    shifts = self.slice_item_shift()

    print(" ," + ",".join(data_set.SHIFT_BOXES))
    for index in range(len(shifts)):
      item = self.list_sale_item[index]
      print( item.name + "," + ','.join(map(str, shifts[index])))

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
        result.append(data_set.SHIFT_BOXES[index])
      index = index + 1
    return result

  # コマ番号を指定してアサインされているユーザ番号リストを取得する
  def get_user_nos_by_box_index(self, box_index):
    user_nos = []
    index = 0
    for line in self.slice_item_shift():
      if line[box_index] == 1:
        user_nos.append(index)
      index += 1
    return user_nos

  # コマ名を指定してアサインされているユーザ番号リストを取得する
  def get_user_nos_by_box_name(self, box_name):
    box_index = data_set.SHIFT_BOXES.index(box_name)
    return self.get_user_nos_by_box_index(box_index)

  # 想定人数と実際の人数の差分を取得する
  def abs_people_between_need_and_actual(self):
    result = []
    index = 0
    for need in data_set.NEED_ITEM:
      actual = len(self.get_user_nos_by_box_index(index))
      result.append(abs(need - actual))
      index += 1
    return result

  # 応募していないコマにアサインされている件数を取得する
  def not_applicated_assign(self):
    count = 0
    for box_name in data_set.SHIFT_BOXES:
      user_nos = self.get_user_nos_by_box_name(box_name)
      for user_no in user_nos:
        e = self.list_sale_item[user_no]
        if not e.is_applicated(box_name):
          count += 1
    return count

  # アサインが応募コマ数の50%に満たないユーザを取得
  def few_work_user(self):
    result = []
    for user_no in range(10):
      e = self.list_sale_item[user_no]
      ratio = float(len(self.get_boxes_by_user(user_no))) / float(len(e.wills))
      if ratio < 0.5:
        result.append(e)
    return result

  # 管理者が1人もいないコマ
  def no_manager_box(self):
    result = []
    for box_name in data_set.SHIFT_BOXES:
      manager_included = False
      user_nos = self.get_user_nos_by_box_name(box_name)
      for user_no in user_nos:
        e = self.list_sale_item[user_no]
        if e.manager:
          manager_included = True
      if not manager_included:
        result.append(box_name)
    return result

