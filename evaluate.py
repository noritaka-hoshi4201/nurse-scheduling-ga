from sale_item import SaleItem
from schedule import Schedule

# FITNESS_RESULT = (-10.0, -100.0, -1.0, -100.0, -10.0)

# 適応度
# 個体の適応度を最大化したい場合は、weights=(1.0,)と書きます。
# 個体の適応度を最小化したい場合は、マイナスを付けてweights=(-1.0,)と書きます。
# 例えば2つある適応度の1つを最大化、もう1つを最小化する場合は、weights=(1.0,-1.0)と書いてやります。
# https://darden.hatenablog.com/entry/2017/04/18/225459
FITNESS_RESULT = (-10.0,
                  -1.0
                  )

def evaluate_item_count(individual) -> tuple:
    """評価関数

    Args:
        individual (_type_): _description_

    Returns:
        tubple: 全てが0になった時が最適解となるようにする
    """
    sche = Schedule(individual)

    # 想定発注数とアサイン発注数の差
    people_count_sub_sum = sum(sche.abs_item_between_need_and_actual()) / sche.len_item_shift_all
    # アサイン数が応募数の半分以下の従業員数
    few_work_user = len(sche.few_work_user()) / 10.0
    return (people_count_sub_sum, # -10.0
            few_work_user        # -1.0
            )

