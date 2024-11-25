"""  """

from sale_item import SaleItem



# コマの定義
SHIFT_BOXES = [
  '月',
  '火',
  '水',
  '木',
  '金',
  '土',
  '日']

LEN_SHIFT = len(SHIFT_BOXES)

# 各コマの想定発注数
NEED_ITEM = [
  7,
  7,
  7,
  7,
  7,
  7,
  7
]


# 従業員定義

# 毎日
e0 = SaleItem(0, "山田", 40, False, 
              ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'])
e1 = SaleItem(1, "鈴木", 21, False, 
              ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'])
e2 = SaleItem(2, "佐藤", 18, False, 
              ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'])
e3 = SaleItem(3, "田中", 35, True, 
              ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'])

# 月水金日
e4 = SaleItem(4, "山口", 19, False, 
              ['mon', 'wed', 'fri', 'sun'])
e5 = SaleItem(5, "加藤", 43, True, 
              ['mon', 'wed', 'fri', 'sun'])
e6 = SaleItem(6, "川口", 25, False, 
              ['mon', 'wed', 'fri', 'sun'])

# 火木土
e7 = SaleItem(7, "野口", 22, False, 
              ['tue', 'thu', 'sat'])
e8 = SaleItem(8, "棚橋", 18, False, 
              ['tue', 'thu', 'sat'])
e9 = SaleItem(9, "小山", 30, True, 
              ['tue', 'thu', 'sat'])

def get_data_set()->tuple:
    return (e0, e1, e2, e3, e4, e5, e6, e7, e8, e9)