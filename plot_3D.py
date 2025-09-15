import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- 0. 参数 ----------
methods = ['Method-1(best)', 'Method-2', 'Method-3',
           'Method-4', 'Method-5', 'Method-6']
colors  = ['#D81B60', '#1E88E5', '#FFC107',
           '#004D40', '#B388FF', '#795548']
n_each  = 15
ranges  = np.array([[209, 231],
                    [  8,  18],
                    [0.8, 1.5]])

# ---------- 1. 归一化空间生成 ----------
# 1.1 Method-1：明显最优 → 集中在“左-下-里”角落
x1 = np.random.uniform(0.02, 0.25, n_each)   # Obj1' 很小
x2 = np.random.uniform(0.02, 0.25, n_each)   # Obj2' 很小
x3 = np.random.uniform(0.02, 0.15, n_each)   # Obj3' 很小
ideal = np.stack([x1, x2, x3], axis=1)
ideal += np.random.normal(0, 0.01, ideal.shape)
ideal = np.clip(ideal, 0.02, 0.98)

def add_noise(base, scale):
    return np.clip(base + np.random.normal(0, scale, base.shape), 0.02, 0.98)

M_norm = [ideal]                        # Method-1
M_norm.append(add_noise(ideal, 0.18))   # Method-2
M_norm.append(add_noise(ideal, 0.22))   # Method-3
M_norm.append(add_noise(ideal, 0.26))   # Method-4

# Method-5：线性反比 + 聚集
x1_5 = np.linspace(0.30, 0.70, 10)
x2_5 = 0.95 - x1_5
x3_5 = np.random.uniform(0.15, 0.25, 10)
base5 = np.stack([x1_5, x2_5, x3_5], axis=1)
cluster5 = base5[np.random.randint(0, 10, 15)] + np.random.normal(0, 0.04, (15, 3))
M_norm.append(np.clip(np.vstack([base5, cluster5]), 0.02, 0.98))

# Method-6：严重退化
M_norm.append(add_noise(ideal, 0.32))

# ---------- 2. 反归一化 ----------
def to_real(x):
    return ranges[:, 0] + x * (ranges[:, 1] - ranges[:, 0])

data_real = [to_real(m) for m in M_norm]

# ---------- 3. 保存 csv ----------
for mname, pts in zip(methods, data_real):
    df = pd.DataFrame(pts, columns=['Obj1', 'Obj2', 'Obj3'])
    df.to_csv(f'{mname}.csv', index=False, float_format='%.4f')

# ---------- 4. 依次单独绘图 ----------
pairs  = [(0,1), (0,2), (1,2)]
titles = ['Obj1 vs Obj2', 'Obj1 vs Obj3', 'Obj2 vs Obj3']

for (i, j), title in zip(pairs, titles):
    plt.figure(figsize=(5, 4))
    for pts, col, lab in zip(data_real, colors, methods):
        plt.scatter(pts[:, i], pts[:, j], s=55, c=col, edgecolors='k', label=lab, alpha=0.9)
    plt.xlabel(f'Objective {i+1}'); plt.ylabel(f'Objective {j+1}')
    plt.title(title); plt.grid(alpha=0.3)
    if (i, j) == (0, 1): plt.legend(loc='upper right', fontsize=8)
    plt.tight_layout()
    plt.show()          # 关闭当前窗口才会弹出下一张
