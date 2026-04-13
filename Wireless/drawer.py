from __future__ import annotations

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
MPL_CONFIG_DIR = PROJECT_DIR / ".mplconfig"
MPL_CONFIG_DIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIR))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator


plt.rcParams["font.sans-serif"] = [
    "PingFang SC",
    "Hiragino Sans GB",
    "Noto Sans CJK SC",
    "Microsoft YaHei",
    "SimHei",
    "Arial Unicode MS",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "stix"


a = [2100, 2180, 2210, 2230, 2260, 2290, 2310, 2340, 2420]  # 单位是kHz
b = [8.500, 10.60, 13.00, 14.50, 16.50, 15.40, 14.90, 15.00, 8.400]  # 单位是V
c = [10, 13, 16, 19, 22, 25, 28, 31]  # 单位是cm
d = [8.400, 14.30, 18.20, 18.30, 16.40, 14.10, 11.70, 10.00]  # 单位是V


def style_axes(ax: plt.Axes, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.tick_params(which="major", length=5, width=0.9, labelsize=10)
    ax.tick_params(which="minor", length=2.5, width=0.6)
    ax.grid(which="major", linestyle="--", linewidth=0.6, alpha=0.35)
    ax.grid(which="minor", linestyle=":", linewidth=0.4, alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_frequency_curve(x_values: list[float], y_values: list[float], output_path: Path) -> None:
    x = np.asarray(x_values, dtype=float)
    y = np.asarray(y_values, dtype=float)
    peak_index = int(np.argmax(y))

    fig, ax = plt.subplots(figsize=(8.2, 5.2), dpi=220)
    ax.plot(
        x,
        y,
        color="#1f5aa6",
        linewidth=2.0,
        marker="o",
        markersize=5.5,
        markerfacecolor="white",
        markeredgewidth=1.2,
    )

    style_axes(ax, "Frequency / kHz", "Vpp / V")
    ax.set_xlim(2080, 2440)
    ax.set_ylim(7.5, 17.5)
    ax.xaxis.set_major_locator(MultipleLocator(40))
    ax.xaxis.set_minor_locator(MultipleLocator(20))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))

    ax.scatter(x[peak_index], y[peak_index], color="#cf3d2e", s=44, zorder=4)
    ax.annotate(
        "Peak\n(2260 kHz, 16.50 V)",
        xy=(x[peak_index], y[peak_index]),
        xytext=(2288, 16.9),
        fontsize=9.5,
        ha="left",
        va="top",
        arrowprops={"arrowstyle": "->", "lw": 0.9, "color": "#555555"},
        bbox={"boxstyle": "round,pad=0.28", "fc": "white", "ec": "#999999", "alpha": 0.92},
    )

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def plot_distance_curve(x_values: list[float], y_values: list[float], output_path: Path) -> None:
    x = np.asarray(x_values, dtype=float)
    y = np.asarray(y_values, dtype=float)
    peak_index = int(np.argmax(y))

    fig, ax = plt.subplots(figsize=(8.2, 5.2), dpi=220)
    ax.plot(
        x,
        y,
        color="#1f5aa6",
        linewidth=2.0,
        marker="s",
        markersize=5.2,
        markerfacecolor="white",
        markeredgewidth=1.1,
    )

    style_axes(ax, "Distance / cm", "Vpp / V")
    ax.set_xlim(9, 32)
    ax.set_ylim(7.5, 19.5)
    ax.xaxis.set_major_locator(MultipleLocator(3))
    ax.xaxis.set_minor_locator(MultipleLocator(1.5))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    ax.scatter(x[peak_index], y[peak_index], color="#cf3d2e", s=44, zorder=4)
    ax.annotate(
        "Peak\n(19 cm, 18.30 V)",
        xy=(x[peak_index], y[peak_index]),
        xytext=(21.2, 18.8),
        fontsize=9.5,
        ha="left",
        va="top",
        arrowprops={"arrowstyle": "->", "lw": 0.9, "color": "#555555"},
        bbox={"boxstyle": "round,pad=0.28", "fc": "white", "ec": "#999999", "alpha": 0.92},
    )

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    plot_frequency_curve(a, b, PROJECT_DIR / "graph1.png")
    plot_distance_curve(c, d, PROJECT_DIR / "graph2.png")
    print("Saved:")
    print(PROJECT_DIR / "graph1.png")
    print(PROJECT_DIR / "graph2.png")


if __name__ == "__main__":
    main()
