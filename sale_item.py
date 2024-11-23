# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), './lib'))


# 従業員を表すクラス
class SaleItem(object):
  def __init__(self, no, name, age, manager, wills):
    self.no = no
    self._name = name
    self.age = age
    self.manager = manager
    # 発注希望日
    self.wills = wills

  @property
  def name(self) -> str:
    return self._name

  def is_applicated(self, box_name):
    return (box_name in self.wills)
