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

from sale_item import SaleItem
from schedule import Schedule

import data_set

import evaluate

# データ読み込み
init_data = Schedule()

creator.create("FitnessItemCount", base.Fitness, weights=init_data.get_eval_fitness())
creator.create("Individual", list, fitness=creator.FitnessItemCount)

toolbox = base.Toolbox()

toolbox.register("map", futures.map)

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, int(init_data.len_item_shift_all))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# resisterでtoolboxに第一変数の名前のメソッドを追加する。
# toolbox.attr_bool: random.randint(0,1)
# toolbox.individual: toolbox.attr_boolを使って01乱数 > tools.initRepeatによって100回繰り返し100要素のリストを作成(=個体生成)
# toolbox.polulation: toolbox.individualによる個体生成を繰り返し、個体集団作成
# https://qiita.com/shigeyuki-m/items/9e395822ac39283f9031

# 評価関数を登録
toolbox.register("evaluate", evaluate.evaluate_item_count)
# 交叉関数を定義(二点交叉)
toolbox.register("mate", tools.cxTwoPoint)

# 変異関数を定義(ビット反転、変異隔離が5%ということ?)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# 選択関数を定義(トーナメント選択、tournsizeはトーナメントの数？)
toolbox.register("select", tools.selTournament, tournsize=3)



if __name__ == '__main__':
    try:
        population, CXPB, MUTPB, NGEN = init_data.get_calc_param() # 交差確率、突然変異確率、進化計算のループ回数

        # 初期集団を生成する
        pop = toolbox.population(n=population) # 1世代内でいくつの個体を持つか？

        # 交叉
        # – 一定確率で二つの「種」の遺伝子配列が組み合わされて新しい種となること

        # 突然変異
        # – 遺伝子配列の中の特定のビットが一定確率で逆転して、別の種となること

        print("進化開始")

        # 初期集団の個体を評価する
        fitnesses = list(map(toolbox.evaluate, pop))
        # print(f"fitnesses: {fitnesses}")
        for ind, fit in zip(pop, fitnesses):  # zipは複数変数の同時ループ
            # print(f"ind.fitness.values: {ind.fitness.values}")
            # print(f"fit: {fit}")
            # 適合性をセットする
            ind.fitness.values = fit

        print("  %i の個体を評価" % len(pop))

        # 進化計算開始
        for g in range(NGEN):
            print("-- %i 世代 --" % g)

            # 選択
            # 次世代の個体群を選択
            offspring = toolbox.select(pop, len(pop))
            # 個体群のクローンを生成
            offspring = list(map(toolbox.clone, offspring))

            # 選択した個体群に交差と突然変異を適応する

            # 交叉
            # 偶数番目と奇数番目の個体を取り出して交差
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    # 交叉された個体の適合度を削除する
                    del child1.fitness.values
                    del child2.fitness.values

            # 変異
            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # 適合度が計算されていない個体を集めて適合度を計算
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            print("  %i の個体を評価" % len(invalid_ind))

            # 次世代群をoffspringにする
            pop[:] = offspring

            # すべての個体の適合度を配列にする
            # print(f"ind.fitness.values: {ind.fitness.values}")
            
            for idx, _val in enumerate(ind.fitness.values):
                fits = [tmp.fitness.values[idx] for tmp in pop]
                # print(f"fits: {fits}")
                length = len(pop)
                mean = sum(fits) / length
                sum2 = sum(x*x for x in fits)
                std = abs(sum2 / length - mean**2)**0.5

                print(f"* パラメータ{idx+1}")
                print("  Min %s" % min(fits))
                print("  Max %s" % max(fits))
                print("  Avg %s" % mean)
                print("  Std %s" % std)

        print("-- 進化終了 --")

        best_ind = tools.selBest(pop, 1)[0]
        print(f"最も優れていた個体: {best_ind.fitness.values}")
        ret_best = Schedule(best_ind)
        ret_best.print_csv()
        path = ret_best.save()
        print(f"save -> {path}")

        print(f"eval count: {init_data.eval_count}")
        # ret_best.print_tsv()
    except Exception as ex:
        print(f"エラーが発生しました: {ex}")
