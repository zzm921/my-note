
import importlib.util, sys, os, numpy as np
from pathlib import Path
ROOT = Path("/tmp/ml-review")

def load(rel):
    p = ROOT / rel
    os.chdir(p.parent)                      # 他们的脚本用相对路径读数据
    spec = importlib.util.spec_from_file_location(p.stem, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[p.stem] = m
    spec.loader.exec_module(m)              # 执行 top-level（含他们的训练）
    return m

import matplotlib; matplotlib.use("Agg")
from sklearn.linear_model import LinearRegression, LogisticRegression

print("=" * 62)
print("验收① 线性回归：损失单调性 + 与 sklearn 的系数/截距差异")
print("=" * 62)
m = load("04_linear_regression/linear_regression.py")
theta, cost = np.asarray(m.theta, dtype=float), np.asarray(m.cost_data, dtype=float)
d = np.diff(cost)
print(f"迭代次数={len(cost)-1}  初始代价={cost[0]:.6f}  最终代价={cost[-1]:.6f}")
print(f"单调不增: {'✅' if np.all(d <= 1e-12) else '❌'}  最大上升步长={d.max():.3e}")
X, y = np.asarray(m.X, float), np.asarray(m.y, float).ravel()
sk = LinearRegression(fit_intercept=False).fit(X, y)
print(f"θ_自己 = {np.round(theta, 6)}")
print(f"θ_sklearn = {np.round(sk.coef_, 6)}")
print(f"最大绝对差 = {np.max(np.abs(theta - sk.coef_)):.3e}  → 标准(<1e-2): "
      f"{'✅ 通过' if np.max(np.abs(theta - sk.coef_)) < 1e-2 else '❌ 未达标'}")
print(f"代价对比: 自己={cost[-1]:.8f}  sklearn MSE/2={np.mean((X@sk.coef_-y)**2)/2:.8f}")

print()
print("=" * 62)
print("验收③ 逻辑回归：与 sklearn 的测试集准确率差距")
print("=" * 62)
m2 = load("05_logistic_regression/logistic_regression.py")
th, X2, y2 = np.asarray(m2.theta, float), np.asarray(m2.X, float), np.asarray(m2.y, float).ravel()
def acc(w, Xd, yd):
    p = 1/(1+np.exp(-(Xd @ w)))
    return float(np.mean((p >= 0.5).astype(int) == yd))
a_self = acc(th, X2, y2)
sk2 = LogisticRegression(max_iter=5000).fit(X2[:, 1:], y2)
a_sk = sk2.score(X2[:, 1:], y2)
print(f"自己实现准确率 = {a_self:.4f}   sklearn 准确率 = {a_sk:.4f}   差 = {abs(a_self-a_sk):.4f}")
print(f"标准(差<2%): {'✅ 通过' if abs(a_self-a_sk) < 0.02 else '❌ 未达标'}")
print(f"θ 自己 = {np.round(th, 4)}")

print()
print("=" * 62)
print("验收④ 特征缩放对收敛的影响（同一 alpha，标准化 vs 未标准化）")
print("=" * 62)
d1 = np.loadtxt(ROOT/"04_linear_regression/ex1data1.txt", delimiter=",")
Xr, yr = d1[:, :1], d1[:, 1]
def gd(X, y, alpha=0.01, n=500):
    m_ = len(y); Xb = np.column_stack([np.ones(m_), X]); th = np.zeros(Xb.shape[1]); hist = []
    for _ in range(n):
        th = th - alpha/m_ * (Xb.T @ (Xb @ th - y)); hist.append(np.mean((Xb@th-y)**2)/2)
    return hist[-1], hist
c_raw, _ = gd(Xr, yr)
c_std, _ = gd((Xr - Xr.mean(0))/Xr.std(0), yr)
print(f"500 次迭代后：未标准化代价={c_raw:.4f}  标准化代价={c_std:.4f}  "
      f"→ {'✅ 标准化明显更快收敛' if c_std < c_raw*0.9 else '⚠️ 差异不明显'}")
