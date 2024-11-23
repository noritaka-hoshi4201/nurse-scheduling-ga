from sale_item import SaleItem
from schedule import Schedule

# FITNESS_RESULT = (-10.0, -100.0, -1.0, -100.0, -10.0)

# 適応度
# 個体の適応度を最大化したい場合は、weights=(1.0,)と書きます。
# 個体の適応度を最小化したい場合は、マイナスを付けてweights=(-1.0,)と書きます。
# 例えば2つある適応度の1つを最大化、もう1つを最小化する場合は、weights=(1.0,-1.0)と書いてやります。
# https://darden.hatenablog.com/entry/2017/04/18/225459
FITNESS_RESULT = (-100.0, -100.0, -1.0, -100.0)

def evaluate_item_count(individual) -> tuple:
    """評価関数

    Args:
        individual (_type_): _description_

    Returns:
        tubple: 全てが0になった時が最適解となるようにする
    """
    s = Schedule(individual)

    # 想定人数とアサイン人数の差
    people_count_sub_sum = sum(s.abs_people_between_need_and_actual()) / 70.0
    # 応募していない曜日へのアサイン数
    not_applicated_count = s.not_applicated_assign() / 70.0
    # アサイン数が応募数の半分以下の従業員数
    few_work_user = len(s.few_work_user()) / 10.0
    # 管理者が１人もいないコマ数
    no_manager_box = len(s.no_manager_box()) / 7.0
    # 朝・昼・夜の全部にアサインされている
    # three_box_per_day = len(s.three_box_per_day()) / 70.0
    # return (not_applicated_count, people_count_sub_sum, few_work_user, no_manager_box, three_box_per_day)
    return (not_applicated_count, # -100.0
            people_count_sub_sum, # -100.0
            few_work_user,        # -1.0
            no_manager_box        # -100.0
            )

