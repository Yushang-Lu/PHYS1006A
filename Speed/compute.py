"""处理《空气中声速的测量》前四部分数据。

用法：
1. 把 a、b、c、d、e 五个数组替换成实测数据。
   其中 a、b、c、d 为位置数据，单位 mm；e 为时间数据，单位 us。
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

# 下面给出可直接运行的示例数据。
# 如果要处理自己的实验结果，直接替换这几个数组即可。
a = [148.286, 153.280, 158.357, 163.061, 168.283, 173.019, 177.971, 182.881, 187.764, 192.763]
b = [153.108, 157.757, 162.768, 167.561, 172.771, 177.354, 182.493, 187.157, 192.331, 196.828]
c = [147.982, 157.719, 167.469, 177.188, 187.018, 196.837, 206.493, 216.239, 226.778, 235.016]
d = [140.000, 150.000, 160.000, 170.000, 180.000, 190.000, 200.000, 210.000, 220.000, 230.000]
e = [458, 482, 516, 546, 574, 602, 628, 660, 688, 716]


@dataclass(frozen=True)
class MethodResult:
    name: str
    data_mm: np.ndarray
    pair_differences_mm: np.ndarray
    lambda_mm: float
    speed_m_per_s: float
    sigma: float


@dataclass(frozen=True)
class TimeDifferenceResult:
    name: str
    positions_mm: np.ndarray
    times_us: np.ndarray
    pair_differences_mm: np.ndarray
    pair_time_differences_us: np.ndarray
    pair_speeds_m_per_s: np.ndarray
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


def analyze_time_difference_method(
    name: str,
    positions_mm: list[float] | np.ndarray,
    times_us: list[float] | np.ndarray,
    theoretical_v0: float,
) -> TimeDifferenceResult:
    """按时差法处理 10 组位置-时间数据。"""
    positions = validate_array("d", positions_mm)
    times = validate_array("e", times_us)
    pair_differences = positions[5:] - positions[:5]
    pair_time_differences = times[5:] - times[:5]

    if np.any(pair_differences <= 0):
        raise ValueError("d 中的数据应随测量次数递增，以保证逐差位移为正。")
    if np.any(pair_time_differences <= 0):
        raise ValueError("e 中的数据应随测量次数递增，以保证逐差时间差为正。")

    # 单位换算：1 mm / us = 1000 m / s。
    pair_speeds = pair_differences / pair_time_differences * 1000.0
    speed_m_per_s = float(np.mean(pair_speeds))
    sigma = abs(speed_m_per_s - theoretical_v0) / theoretical_v0
    return TimeDifferenceResult(
        name=name,
        positions_mm=positions,
        times_us=times,
        pair_differences_mm=pair_differences,
        pair_time_differences_us=pair_time_differences,
        pair_speeds_m_per_s=pair_speeds,
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


def print_time_difference_result(result: TimeDifferenceResult) -> None:
    """打印时差法的计算结果。"""
    positions = [round(value, 3) for value in result.positions_mm.tolist()]
    times = [round(value, 3) for value in result.times_us.tolist()]
    diffs = [round(value, 3) for value in result.pair_differences_mm.tolist()]
    time_diffs = [round(value, 3) for value in result.pair_time_differences_us.tolist()]
    pair_speeds = [round(value, 3) for value in result.pair_speeds_m_per_s.tolist()]

    print(result.name)
    print(f"原始数据 l_i(mm) = {positions}")
    print(f"原始数据 t_i(us) = {times}")
    print(f"逐差 l_(i+5)-l_i(mm) = {diffs}")
    print(f"逐差 t_(i+5)-t_i(us) = {time_diffs}")
    print(f"逐差速度 v_i(m/s) = {pair_speeds}")
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
    time_difference_result = analyze_time_difference_method(
        name="时差法测空气中声速",
        positions_mm=d,
        times_us=e,
        theoretical_v0=v0,
    )

    print(f"室温 t = {ROOM_TEMPERATURE_C:.2f} °C")
    print(f"频率 f = {FREQUENCY_KHZ:.3f} kHz")
    print(f"理论声速 v_0 = {v0:.2f} m/s")
    print()

    for result in results:
        print_result(result)
    print_time_difference_result(time_difference_result)


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"输入数据错误：{exc}")
        raise SystemExit(1) from exc
