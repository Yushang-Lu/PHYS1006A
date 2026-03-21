import numpy as np


def log_voltage_gap(uc_values, source_voltage):
    """返回过冲峰值对应的 ln(U_C - E)。"""
    uc_array = np.asarray(uc_values, dtype=float)
    gaps = uc_array - float(source_voltage)
    if np.any(gaps <= 0):
        raise ValueError("对于测得的峰值，U_C 必须大于 E。")
    return np.log(gaps)


def least_squares_line(x_values, y_values):
    """
    使用正规方程拟合 y = k0 + k1 * x，
    即 K = (A^T A)^(-1) A^T Y，其中 A 的每一行为 [1, x_i]。
    """
    x_array = np.asarray(x_values, dtype=float)
    y_array = np.asarray(y_values, dtype=float)

    if x_array.shape != y_array.shape:
        raise ValueError("x_values 和 y_values 的长度必须相同。")
    if x_array.size < 2:
        raise ValueError("至少需要两个数据点。")

    design_matrix = np.column_stack((np.ones_like(x_array), x_array))
    normal_matrix = design_matrix.T @ design_matrix
    rhs = design_matrix.T @ y_array
    return np.linalg.solve(normal_matrix, rhs)


def main():
    # 来自 rlc.tex 的实验峰值数据
    t_us = np.array([2.80, 9.60, 16.6, 23.6, 30.4], dtype=float)
    uc_v = np.array([14.3, 13.9, 13.4, 13.0, 12.6], dtype=float)
    e_v = 10.0

    ln_uc_minus_e = log_voltage_gap(uc_v, e_v)
    k0, k1 = least_squares_line(t_us, ln_uc_minus_e)

    # 根据 ln(U_C - E) = k0 + k1 t = ln(A) - t / tau 计算时间常数
    tau_us = -1.0 / k1
    tau_s = tau_us * 1e-6
    decay_rate_per_s = -k1 * 1e6

    print("t（us）：", t_us.tolist())
    print("U_C（V）：", uc_v.tolist())
    print("ln(U_C - E)：", np.round(ln_uc_minus_e, 6).tolist())
    print(f"k0 = {k0:.6f}")
    print(f"k1 = {k1:.8f} 1/us")
    print(f"1/tau = {-k1:.8f} 1/us = {decay_rate_per_s:.2f} 1/s")
    print(f"tau = {tau_us:.6f} us = {tau_s:.8e} s")


if __name__ == "__main__":
    main()
