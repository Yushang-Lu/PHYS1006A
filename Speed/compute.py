"""处理《空气中声速的测量》前三部分数据。

用法：
1. 把 a、b、c 三个数组替换成 10 个实测位置数据，单位统一为 mm。
2. 按需要修改室温和频率。
3. 运行：
   conda run --no-capture-output -n tf2 python Speed/compute.py

说明：
- 极值法、相位比较法中，相邻两次记录相隔半个波长。
- 波形移动法中，相邻两次记录相隔一个波长。
- speed.tex 中公式部分写的是 f = 35.555 kHz，脚本默认按这个值计算。
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


ROOM_TEMPERATURE_C = 25.0
FREQUENCY_KHZ = 35.555
# 注意：
# 1. 25 °C 代入 v0 = 331.45 * sqrt(1 + t / 273.15) 得到约 346.29 m/s。
# 2. speed.tex 中给出的部分示例数值与上述公式/频率并不完全一致。
# 脚本这里按公式和常量本身严格计算，若要复现实验报告中的特定结果，
# 请以你的实测温度和实际频率为准修改 ROOM_TEMPERATURE_C、FREQUENCY_KHZ。

# 下面给出三组可直接运行的示例数据，单位 mm。
# 如果要处理自己的实验结果，直接替换这三个数组即可。
a = [148.286, 153.280, 158.357, 163.061, 168.283, 173.019, 177.971, 182.881, 187.764, 192.763]
b = [153.108, 157.757, 162.768, 167.561, 172.771, 177.354, 182.493, 187.157, 192.331, 196.828]
c = [147.982, 157.719, 167.469, 177.188, 187.018, 196.837, 206.493, 216.239, 226.778, 235.016]


@dataclass(frozen=True)
class MethodResult:
    name: str
    data_mm: np.ndarray
    pair_differences_mm: np.ndarray
    lambda_mm: float
    speed_m_per_s: float
    sigma: float


def validate_array(name: str, values: list[float] | np.ndarray) -> np.ndarray:
    """检查输入数组是否为 10 个有效数值。"""
    array = np.asarray(values, dtype=float)
    if array.shape != (10,):
        raise ValueError(f"{name} 必须恰好包含 10 个数据，当前形状为 {array.shape}。")
    if np.isnan(array).any():
        raise ValueError(f"{name} 中仍有占位 nan，请替换成 10 个实测位置数据后再运行。")
    return array


def theoretical_speed(temperature_c: float) -> float:
    """计算室温下空气中的理论声速 v0。"""
    return 331.45 * math.sqrt(1.0 + temperature_c / 273.15)


def analyze_method(
    name: str,
    values_mm: list[float] | np.ndarray,
    pair_wavelength_count: float,
    frequency_khz: float,
    theoretical_v0: float,
) -> MethodResult:
    """按逐差法处理一组 10 点数据。"""
    data = validate_array(name, values_mm)
    pair_differences = data[5:] - data[:5]
    lambda_mm = float(np.sum(pair_differences) / (5 * pair_wavelength_count))
    speed_m_per_s = lambda_mm * frequency_khz
    sigma = abs(speed_m_per_s - theoretical_v0) / theoretical_v0
    return MethodResult(
        name=name,
        data_mm=data,
        pair_differences_mm=pair_differences,
        lambda_mm=lambda_mm,
        speed_m_per_s=speed_m_per_s,
        sigma=sigma,
    )


def print_result(result: MethodResult) -> None:
    """打印单种方法的计算结果。"""
    raw = [round(value, 3) for value in result.data_mm.tolist()]
    diffs = [round(value, 3) for value in result.pair_differences_mm.tolist()]

    print(result.name)
    print(f"原始数据 l_i(mm) = {raw}")
    print(f"逐差 l_(i+5)-l_i(mm) = {diffs}")
    print(f"\\bar{{lambda}} = {result.lambda_mm:.4f} mm")
    print(f"v = {result.speed_m_per_s:.2f} m/s")
    print(f"sigma = {result.sigma:.2%}")
    print()


def main() -> None:
    v0 = theoretical_speed(ROOM_TEMPERATURE_C)
    results = [
        analyze_method(
            name="极值法（驻波法）",
            values_mm=a,
            pair_wavelength_count=2.5,
            frequency_khz=FREQUENCY_KHZ,
            theoretical_v0=v0,
        ),
        analyze_method(
            name="相位比较法",
            values_mm=b,
            pair_wavelength_count=2.5,
            frequency_khz=FREQUENCY_KHZ,
            theoretical_v0=v0,
        ),
        analyze_method(
            name="波形移动法",
            values_mm=c,
            pair_wavelength_count=5.0,
            frequency_khz=FREQUENCY_KHZ,
            theoretical_v0=v0,
        ),
    ]

    print(f"室温 t = {ROOM_TEMPERATURE_C:.2f} °C")
    print(f"频率 f = {FREQUENCY_KHZ:.3f} kHz")
    print(f"理论声速 v_0 = {v0:.2f} m/s")
    print()

    for result in results:
        print_result(result)


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"输入数据错误：{exc}")
        raise SystemExit(1) from exc
