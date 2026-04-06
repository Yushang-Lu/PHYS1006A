import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
MPL_CONFIG_DIR = PROJECT_DIR / ".mplconfig"
MPL_CONFIG_DIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIR))

import matplotlib
import numpy as np


matplotlib.use("Agg")

import matplotlib.pyplot as plt


plt.rcParams["font.sans-serif"] = [
    "PingFang SC",
    "Hiragino Sans GB",
    "Noto Sans CJK SC",
    "SimHei",
    "Arial Unicode MS",
]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "stix"


# Fill `a` and `b` by directly replacing the 30 numbers below.
# The format can be either a Python list or a NumPy array.
# a是加热面热电偶电势，b是中心面热电偶电势，单位都是 μV。
# 这里换算得到的是相对于参考端（通常近似室温）的温差/温升，而不是绝对温度。
# k 是热电偶比例系数，单位为 μV/°C。
a = [
    92, 150, 181, 207, 230, 253,
    275, 297, 318, 340, 361, 382,
    403, 424, 444, 464, 484, 503,
    522, 541, 559, 577, 594, 612,
    629, 645, 661, 676, 692, 707,
]
b = [
    96, 101, 114, 132, 153, 174,
    196, 217, 238, 260, 281, 302,
    323, 344, 364, 385, 405, 424,
    443, 462, 481, 498, 516, 533,
    550, 567, 583, 599, 614, 629,
]
k = 40


def validate_array(name: str, values: np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.shape != (30,):
        raise ValueError(f"{name} must contain exactly 30 values, got shape {array.shape}.")
    return array


def plot_series(x: np.ndarray, y: np.ndarray, title: str, ylabel: str, output_path: Path) -> None:
    plt.figure(figsize=(10, 5), dpi=150)
    plt.plot(x, y, marker="o", linewidth=1.8, markersize=4)
    plt.title(title)
    plt.xlabel(r"时间 $\tau$ (min)")
    plt.ylabel(ylabel)
    plt.xticks(x)
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    a_values = validate_array("a", a)
    b_values = validate_array("b", b)

    x = np.arange(30)
    # c、d 分别表示加热面和中心面相对于参考端的温升。
    c = a_values / k
    d = b_values / k
    diff = c - d

    output_dir = PROJECT_DIR
    plot_series(
        x,
        c,
        r"加热面温升-$\tau$ 曲线",
        r"加热面相对参考端温升 ($K$)",
        output_dir / "heat_curve.png",
    )
    plot_series(
        x,
        d,
        r"中心面温升-$\tau$ 曲线",
        r"中心面相对参考端温升 ($K$)",
        output_dir / "central_curve.png",
    )
    plot_series(x, diff, r"$\Delta T-\tau$ 曲线", r"温差 ($K$)", output_dir / "heat_minus_central_curve.png")

    print("Saved:")
    print(output_dir / "heat_curve.png")
    print(output_dir / "central_curve.png")
    print(output_dir / "heat_minus_central_curve.png")


if __name__ == "__main__":
    main()
