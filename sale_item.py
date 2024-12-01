# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), './lib'))


class SaleItem(object):
  """_summary_

  Args:
      object (_type_): _description_
  """

  def __init__(self, jan, name, pri, will):
    self._jan = str(jan)
    self._name = name if name is None else str(jan)
    if isinstance(pri, int) or isinstance(pri, str) and len(pri)>0:
      self._pri = int(pri)
    else:
      self._pri = 1

    # 発注希望数
    self._will = int(will)

  @property
  def jan(self) -> str:
    return self._jan

  @property
  def name(self) -> str:
    return self._name

  @property
  def priority(self) -> int:
    return self._pri


  @property
  def will(self) -> int:
    return self._will