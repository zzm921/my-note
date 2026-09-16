
"""M2 验收（sklearn-free）：正规方程解析解 + 数值梯度校验"""
import importlib.util, sys, os, numpy as np
from pathlib import Path
ROOT = Path("/tmp/ml-review")

def load(rel):
    p = ROOT / rel
    os.chdir(p.parent)
    spec = importlib.util.spec_from_file_location(p.stem, p)
    m = importlib.util.module_from_spec(spec); sys.modules[p.stem] = m
    spec.loader.exec_module(m)
    return m
import matplotlib; matplotlib.use("Agg")

print("=" * 64)
print("验收① 线性回归：损失单调性 + 与【正规方程解析解】对比（不用 sklearn）")
print("=" * 64)
m = load("04_linear_regression/linear_regression.py")
theta, cost = np.asarray(m.theta, float), np.asarray(m.cost_data, float)
X, y = np.asarray(m.X, float), np.asarray(m.y, float).ravel()
d = np.diff(cost)
print(f"迭代={len(cost)-1}  初始代价={cost[0]:.6f}  最终代价={cost[-1]:.6f}")
print(f"单调不增: {'✅' if np.all(d <= 1e-12) else '❌'}  (最大上升步长 {d.max():.2e})")
theta_ne = np.linalg.pinv(X.T @ X) @ X.T @ y          # 正规方程（closed form）
print(f"θ_梯度下降 = {np.round(theta, 6)}")
print(f"θ_正规方程 = {np.round(theta_ne, 6)}")
print(f"最大绝对差 = {np.max(np.abs(theta - theta_ne)):.2e} → 标准(<1e-2): "
      f"{'✅ 通过' if np.max(np.abs(theta-theta_ne)) < 1e-2 else ''}")
print(f"代价校验: 自己={cost[-1]:.8f}  解析解={np.mean((X@theta_ne-y)**2)/2:.8f}")

print()
print("=" * 64)
print("验收③ 逻辑回归：数值梯度校验（有限差分 vs 解析梯度）+ 收敛与准确率")
print("=" * 64)
m2 = load("05_logistic_regression/logistic_regression.py")
th, X2, y2 = np.asarray(m2.theta, float), np.asarray(m2.X, float), np.asarray(m2.y, float).ravel()
def J(w):                       # 独立实现的代价（对数损失 + 无正则）
    z = X2 @ w; return float(np.mean(np.logaddexp(0, z) - y2 * z))
def grad(w):
    p = 1/(1+np.exp(-(X2 @ w))); return X2.T @ (p - y2) / len(y2)
g_an = grad(th)
num = np.zeros_like(th)         # 有限差分梯度
for k in range(len(th)):
    e = np.zeros_like(th); e[k] = 1e-6
    num[k] = (J(th+e) - J(th-e)) / 2e-6
print(f"解析梯度 = {np.round(g_an, 6)}")
print(f"数值梯度 = {np.round(num, 6)}")
print(f"梯度最大差 = {np.max(np.abs(g_an-num)):.2e} → 实现正确性: "
      f"{'✅ 通过' if np.max(np.abs(g_an-num)) < 1e-6 else '❌'}")
print(f"最优处梯度范数 = {np.linalg.norm(g_an):.2e} → 收敛判据: "
      f"{'✅ 已收敛到极值' if np.linalg.norm(g_an) < 1e-2 else '⚠️ 未完全收敛'}")
p = 1/(1+np.exp(-(X2 @ th))); acc = float(np.mean((p >= 0.5).astype(int) == y2))
print(f"训练集准确率 = {acc:.4f}（吴恩达 ex2 课程参考值 ≈ 0.89）→ "
      f"{'✅ 达到课程水平' if acc >= 0.85 else '⚠️ 偏低'}")

print()
print("=" * 64)
print("验收④ 标准化 vs 未标准化：达到同等代价所需迭代数（严谨版）")
print("=" * 64)
d1 = np.loadtxt(ROOT/"04_linear_regression/ex1data1.txt", delimiter=",")
Xr, yr = d1[:, :1], d1[:, 1]
def gd_hist(X, y, alpha, n=4000):
    Xb = np.column_stack([np.ones(len(y)), X]); th_ = np.zeros(Xb.shape[1]); h = []
    for _ in range(n):
        th_ = th_ - alpha/len(y) * (Xb.T @ (Xb @ th_ - y)); h.append(np.mean((Xb@th_-y)**2)/2)
    return np.array(h)
target = 4.50                                   # 接近最优代价 4.4769
try:
    h_raw = gd_hist(Xr, yr, 0.005)              # 未缩放用更小的 α（大 α 会发散）
    h_std = gd_hist((Xr - Xr.mean(0))/Xr.std(0), yr, 0.005)
    n_raw = int(np.argmax(h_raw <= target)) if (h_raw <= target).any() else -1
    n_std = int(np.argmax(h_std <= target)) if (h_std <= target).any() else -1
    print(f"α=0.005：未标准化到达代价 {target} 需 {n_raw if n_raw>=0 else '>4000'} 次迭代；"
          f"标准化需 {n_std if n_std>=0 else '>4000'} 次")
    print(f"→ {'✅ 标准化明显更快（可复现的缩放收益）' if 0 <= n_std < (n_raw if n_raw>=0 else 9999) else '⚠️ 需调整参数再试'}")
except Exception as e:
    print("测试异常:", e)
for a in (0.01, 0.02, 0.05):
    h = gd_hist(Xr, yr, a, 300)
    print(f"  未标准化 α={a}: 300 次后代价={h[-1]:.2f} {'（发散！）' if not np.isfinite(h[-1]) or h[-1] > 100 else ''}")
