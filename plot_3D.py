import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
# ---------- 0. 参数 ----------
methods = ['MORL_TD', 'PCN', 'GPI_LS',
           'GPI_PD', 'MORL_E', 'MORL_S']
methods_ = ['MORL/TD', 'PCN', 'GPI/LS',
           'GPI/PD', 'MORL/E', 'MORL/S']
colors  = ['#E01B22', '#27D3F5', '#D91BE0',
           '#6CF527', '#F5B027', '#795548']
n_each  = 10                          # ← 只改这里：10 个解
ranges  = np.array([[209, 231],
                    [21 ,  25],
                    [0.8, 1.2]])

# k = (21 - 25) / (231 - 209)   # 共同斜率
# # 单位方向向量（沿斜线）
# dx, dy = 1, k
# norm = np.hypot(dx, dy)
# ux, uy = dx / norm, dy / norm   # 沿斜线方向
# vx, vy = -uy, ux                # 垂直于斜线方向（仅用于可视化检查）

# # ---------- 1. 生成 Method-1：整体最优，但留“缺口” ----------
# # 1.1 沿斜线均匀撒点 + 随机步长
# t = np.linspace(0, 1, n_each)
# x1_m1 = 209 + t * (231 - 209) + np.random.normal(0, 0.8, n_each)
# x1_m1 = np.clip(x1_m1, 209, 231)
# # 1.2 严格落在斜线上，再沿斜线方向加小抖动
# x2_m1 = 25 + k * (x1_m1 - 209) + np.random.normal(0, 0.10, n_each)
# x2_m1 = np.clip(x2_m1, 21, 25)
# # 1.3 Obj3 整体最小，但随机挑 5 个点变差
# x3_m1 = np.random.uniform(0.80, 0.87, n_each)
# bad = np.random.choice(n_each, 5, replace=False)
# x3_m1[bad] = np.random.uniform(0.92, 1.00, 5)
# m1 = np.vstack([x1_m1, x2_m1, x3_m1]).T

# # ---------- 2. 其余方法：同斜率 + 沿斜线随机抖动 ----------
# def gen_method(seed):
#     rng = np.random.default_rng(seed)
#     # 沿斜线随机起点
#     t = rng.uniform(0, 1, n_each)
#     x1 = 209 + t * (231 - 209) + rng.normal(0, 1.2, n_each)
#     x1 = np.clip(x1, 209, 231)
#     x2 = 25 + k * (x1 - 209) + rng.normal(0, 0.12, n_each)
#     x2 = np.clip(x2, 21, 25)
#     # Obj3 随机波动，整体比 Method-1 差
#     x3 = rng.uniform(0.85, 1.15, n_each)
#     return np.vstack([x1, x2, x3]).T

# data_real = [m1] + [gen_method(seed) for seed in range(1, 6)]

# # ---------- 3. 保存 csv ----------
# for mname, pts in zip(methods, data_real):
#     pd.DataFrame(pts, columns=['Time', 'Energy', 'Comfort']).to_csv(
#         f'{mname}.csv', index=False, float_format='%.4f')

# ---------- 4. 依次单独绘图 ----------


# 读取列表
data_real = []
for m in methods:
    file = f'{m}.csv'
    if not os.path.exists(file):
        raise FileNotFoundError(f'{file} 不存在！')
    data_real.append(pd.read_csv(file).values)

pairs  = [(0,1), (0,2), (1,2)]

ticks = [np.arange(205, 236, 5),      # Obj1
         np.arange(21, 27, 2),         # Obj2
         np.arange(0.8, 1.21, 0.1)]   # Obj3

for (i, j) in pairs:
    plt.figure(figsize=(5, 4))
    for pts, col, lab in zip(data_real, colors, methods_):
        plt.scatter(pts[:, i], pts[:, j], s=60, c=col,
                    edgecolors='k', label=lab, alpha=0.9)

    #plt.xlabel(f'Objective {i+1}')
    #plt.ylabel(f'Objective {j+1}')
    plt.grid(alpha=0.3)

    # 固定刻度
    plt.xticks(ticks[i])
    plt.yticks(ticks[j])
    #plt.xlim(200, 240)
    plt.ylim(ticks[j][0], ticks[j][-1])


    plt.legend(loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.show()          # 关        # 关闭当前窗口才会弹出下一张
