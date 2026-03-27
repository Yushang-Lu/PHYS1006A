from __future__ import annotations

import os
import tempfile
from pathlib import Path

import numpy as np

# 避免 matplotlib 因默认配置目录不可写而报 warning
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "mplconfig"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# 在这里替换成你的 10 组实验数据
X = np.array([200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000], dtype=float)
Y = np.array([196.1, 392.2, 595.2, 781.2, 980.4, 1190, 1389, 1562, 1786, 1961], dtype=float)


def least_squares_line(x_values: np.ndarray, y_values: np.ndarray) -> tuple[float, float]:
    """最小二乘拟合直线 y = slope * x + intercept。"""
    x_array = np.asarray(x_values, dtype=float)
    y_array = np.asarray(y_values, dtype=float)

    if x_array.shape != y_array.shape:
        raise ValueError("X 和 Y 的长度必须相同。")
    if x_array.size != 10:
        raise ValueError("按题意要求，X 和 Y 都应包含 10 个元素。")

    design_matrix = np.column_stack((x_array, np.ones_like(x_array)))
    slope, intercept = np.linalg.lstsq(design_matrix, y_array, rcond=None)[0]
    return float(slope), float(intercept)


def build_limits(values: np.ndarray, major_step: float = 200, padding_ratio: float = 0.08) -> tuple[float, float]:
    """根据数据范围生成对齐到大刻度的坐标轴上下限。"""
    min_value = float(np.min(values))
    max_value = float(np.max(values))
    span = max(max_value - min_value, major_step)
    padding = max(major_step / 2, span * padding_ratio)

    lower = major_step * np.floor((min_value - padding) / major_step)
    upper = major_step * np.ceil((max_value + padding) / major_step)
    return lower, upper


def format_equation(slope: float, intercept: float) -> str:
    sign = "+" if intercept >= 0 else "-"
    return f"Y = {slope:.4f}X {sign} {abs(intercept):.2f}"


def main() -> None:
    slope, intercept = least_squares_line(X, Y)

    x_min, x_max = build_limits(X)
    y_min, y_max = build_limits(Y)

    fit_x = np.linspace(x_min, x_max, 400)
    fit_y = slope * fit_x + intercept

    fig, ax = plt.subplots(figsize=(8, 6), dpi=200)

    ax.scatter(X, Y, color="black", s=28, zorder=3)
    ax.plot(fit_x, fit_y, color="tab:red", linewidth=1.8, zorder=2)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("X (Hz)")
    ax.set_ylabel("Y (Hz)")

    ax.xaxis.set_major_locator(MultipleLocator(200))
    ax.yaxis.set_major_locator(MultipleLocator(200))
    ax.xaxis.set_minor_locator(MultipleLocator(50))
    ax.yaxis.set_minor_locator(MultipleLocator(50))

    ax.tick_params(which="major", length=6, width=1)
    ax.tick_params(which="minor", length=3, width=0.8)
    ax.grid(which="major", linestyle="--", linewidth=0.6, alpha=0.55)
    ax.grid(which="minor", linestyle=":", linewidth=0.35, alpha=0.3)

    ax.text(
        0.98,
        0.96,
        format_equation(slope, intercept),
        transform=ax.transAxes,
        ha="right",
        va="top",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "black", "alpha": 0.9},
    )

    fig.tight_layout()

    output_path = Path(__file__).with_name("diagram.png")
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)

    print(f"拟合方程：{format_equation(slope, intercept)}")
    print(f"图像已保存到：{output_path}")


if __name__ == "__main__":
    main()
