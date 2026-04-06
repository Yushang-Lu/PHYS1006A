"""计算准稳态区间内的 Delta T 和 dT/dtau。

计算方法：
1. 读取 drawer.py 中的 a、b、k，并换算得到
   c = a / k, d = b / k。
   其中 c、d 分别表示加热面和中心面相对于参考端的温升。
2. 根据图像判断系统约在 tau = 7 min 后进入准稳态，
   这里取 tau = 7~14 min 作为准稳态分析区间。
3. 只使用该准稳态区间内的数据点，分别对 c-tau 曲线和 d-tau 曲线
   用最小二乘法做一次直线拟合。
4. 拟合直线的斜率近似为各测点的 dT/dtau。
5. 由于准稳态时两条曲线应近似平行，故取两条拟合直线斜率的平均值
   作为样品的 dT/dtau。
6. 取同一区间内 (c - d) 的平均值作为 Delta T。
"""

from __future__ import annotations

import numpy as np

from drawer import a, b, k, validate_array


QUASI_STEADY_START = 7
QUASI_STEADY_END = 14


def least_squares_fit_line(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """用最小二乘法拟合 y = mx + b，返回斜率、截距和 R^2。"""
    x_mean = float(np.mean(x))
    y_mean = float(np.mean(y))
    denominator = float(np.sum((x - x_mean) ** 2))
    if denominator == 0:
        raise ValueError("Least-squares fit requires at least two distinct x values.")

    slope = float(np.sum((x - x_mean) * (y - y_mean)) / denominator)
    intercept = y_mean - slope * x_mean
    fitted = slope * x + intercept
    residual_sum = np.sum((y - fitted) ** 2)
    total_sum = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1.0 if total_sum == 0 else 1 - residual_sum / total_sum
    return slope, float(intercept), float(r_squared)


def main() -> None:
    a_values = validate_array("a", a)
    b_values = validate_array("b", b)

    tau = np.arange(30, dtype=float)
    c = a_values / k
    d = b_values / k
    delta_t = c - d

    window = slice(QUASI_STEADY_START, QUASI_STEADY_END + 1)
    tau_window = tau[window]
    c_window = c[window]
    d_window = d[window]
    delta_t_window = delta_t[window]

    heat_slope, heat_intercept, heat_r2 = least_squares_fit_line(tau_window, c_window)
    center_slope, center_intercept, center_r2 = least_squares_fit_line(tau_window, d_window)

    # 准稳态时两条温升曲线近似平行，因此取两者斜率平均值。
    dT_dtau = (heat_slope + center_slope) / 2
    delta_t_mean = float(np.mean(delta_t_window))
    delta_t_std = float(np.std(delta_t_window, ddof=1))

    print("计算方法：")
    print("1. 用 c = a / k, d = b / k 将热电偶电势换算成相对参考端温升。")
    print(
        f"2. 由图判断准稳态区间取 tau = {QUASI_STEADY_START}~{QUASI_STEADY_END} min。"
    )
    print("3. 只取该区间内的数据点参与最小二乘直线拟合。")
    print("4. 分别得到加热面和中心面温升曲线的斜率。")
    print("5. 取两条拟合直线斜率的平均值作为 dT/dtau。")
    print("6. 取同一区间内 (c-d) 的平均值作为 Delta T。")
    print()

    print("参与拟合的数据点：")
    print(f"tau = {tau_window.tolist()}")
    print(f"c   = {[round(value, 3) for value in c_window.tolist()]}")
    print(f"d   = {[round(value, 3) for value in d_window.tolist()]}")
    print()

    print("拟合结果：")
    print(
        f"加热面: slope = {heat_slope:.5f} °C/min, "
        f"intercept = {heat_intercept:.5f}, R^2 = {heat_r2:.5f}"
    )
    print(
        f"中心面: slope = {center_slope:.5f} °C/min, "
        f"intercept = {center_intercept:.5f}, R^2 = {center_r2:.5f}"
    )
    print()

    print("最终结果：")
    print(f"Delta T ≈ {delta_t_mean:.3f} °C")
    print(f"Delta T 的样本标准差 ≈ {delta_t_std:.3f} °C")
    print(f"dT/dtau ≈ {dT_dtau:.3f} °C/min")


if __name__ == "__main__":
    main()
