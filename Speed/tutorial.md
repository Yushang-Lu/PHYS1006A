# 空气中声速的测量

## `speed.tex`, `compute.py` 食用说明

本目录包含一份大学物理实验报告 LaTeX 模版，以及与之配套的数据处理脚本。

目前文件分工如下：

- `speed.tex`：实验报告正文模版
- `compute.py`：处理前四部分“空气中声速测量”数据，并计算理论值、测量值和相对误差
- `pic1.png`：实验预习部分用到的示意图

建议的使用顺序是：

1. 在 `compute.py` 中填入实验数据，并确认室温与频率
2. 运行 `compute.py` 得到四种方法对应的计算结果
3. 将原始数据和计算结果整理到 `speed.tex`
4. 如需完成“时差法测固体中声速（选做）”，再手动补充该部分数据处理
5. 编译 `speed.tex` 生成实验报告 PDF

## 1. 环境准备

本项目默认使用你已有的 `tf2` conda 环境运行 Python 脚本。

进入项目根目录：

```bash
cd /Users/jinana/PHYS1006A
```

如果要运行 Python 脚本，推荐直接使用：

```bash
conda run --no-capture-output -n tf2 python Speed/compute.py
```

如果你已经手动激活了环境，也可以这样运行：

```bash
conda activate tf2
python Speed/compute.py
```

如果你只编译 LaTeX，而不运行 Python，那么不需要激活 conda 环境。

## 2. `compute.py` 的作用与用法

`compute.py` 负责处理以下四部分实验数据：

- 极值法（驻波法）测空气中声速
- 相位比较法测空气中声速
- 波形移动法测空气中声速
- 时差法测空气中声速

它会同时计算：

- 室温下空气中的理论声速 `v_0`
- 各方法对应的平均波长 `\bar{\lambda}`（前三种方法）
- 各方法对应的声速 `v`
- 各方法测量值与理论值的相对误差 `\sigma`

### 2.1 需要修改的内容

打开 [compute.py](/Users/jinana/PHYS1006A/Speed/compute.py)，重点修改以下几项：

- `ROOM_TEMPERATURE_C = 25.0`
- `FREQUENCY_KHZ = 35.555`
- `a = [...]`
- `b = [...]`
- `c = [...]`
- `d = [...]`
- `e = [...]`

其中：

- `ROOM_TEMPERATURE_C` 表示实验时室温，单位是 `°C`
- `FREQUENCY_KHZ` 表示实验中使用的超声频率，单位是 `kHz`
- `a` 表示极值法（驻波法）记录的 10 个位置数据，单位是 `mm`
- `b` 表示相位比较法记录的 10 个位置数据，单位是 `mm`
- `c` 表示波形移动法记录的 10 个位置数据，单位是 `mm`
- `d` 表示时差法测空气中声速时记录的 10 个位置数据，单位是 `mm`
- `e` 表示与 `d` 一一对应的 10 个传播时间数据，单位是 `μs`

注意：

- `a`、`b`、`c`、`d`、`e` 都必须正好有 `10` 个数
- `a` 到 `d` 的单位统一是 `mm`
- `e` 的单位是 `μs`
- `d` 和 `e` 必须按同一组测量顺序一一对应
- 当前脚本里给的是可直接运行的示例数据，正式写报告前建议全部替换成你自己的实测值

### 2.2 当前脚本采用的计算方法

对于前三种方法，脚本使用逐差法处理数据。

核心思路是：

1. 取后 5 个数据与前 5 个数据逐项作差
2. 由逐差结果求平均波长 `\bar{\lambda}`
3. 用 `v = \bar{\lambda} f` 计算声速
4. 用 `\sigma = |v-v_0|/v_0` 计算相对误差

在代码中，对应的是：

```python
pair_differences = data[5:] - data[:5]
lambda_mm = np.sum(pair_differences) / (5 * pair_wavelength_count)
speed_m_per_s = lambda_mm * frequency_khz
sigma = abs(speed_m_per_s - theoretical_v0) / theoretical_v0
```

其中：

- 极值法和相位比较法取 `pair_wavelength_count = 2.5`
- 波形移动法取 `pair_wavelength_count = 5.0`

对于时差法，脚本按下面的方式计算：

```python
pair_differences = positions[5:] - positions[:5]
pair_time_differences = times[5:] - times[:5]
pair_speeds = pair_differences / pair_time_differences * 1000.0
speed_m_per_s = np.mean(pair_speeds)
```

这里乘 `1000.0` 是因为：

- `1 mm / μs = 1000 m / s`

理论声速 `v_0` 的计算公式为：

```python
v0 = 331.45 * math.sqrt(1.0 + temperature_c / 273.15)
```

另外需要注意：

- `compute.py` 当前只处理“空气中声速测量”的前四部分
- `speed.tex` 最后那个“时差法测固体中声速（选做）”部分并没有在脚本中自动计算

### 2.3 运行方式

在项目根目录运行：

```bash
conda run --no-capture-output -n tf2 python Speed/compute.py
```

### 2.4 输出内容

运行后终端会输出：

- 当前采用的室温 `t`
- 当前采用的频率 `f`
- 理论声速 `v_0`
- 四种方法各自的原始数据
- 逐差结果
- `\bar{\lambda}`、`v`、`\sigma`

这些结果可以直接整理到 [speed.tex](/Users/jinana/PHYS1006A/Speed/speed.tex) 的“数据处理”部分。

## 3. `speed.tex` 的作用与用法

`speed.tex` 是实验报告的主文件。

目前它已经完成了这些工作：

- 设置了报告版式和页眉页脚
- 预留了“实验预习”“实验现象及原始数据记录”“数据处理”“实验结论及现象分析”“讨论题”等部分
- 自动插入实验预习部分需要的 `pic1.png`
- 在“数据处理”中给出了示例公式和一组示例结果

### 3.1 你通常需要修改哪些部分

建议重点检查和修改：

- 页首的班级、学号、姓名、实验日期
- `\section{实验预习}` 中的推导与表格填写
- `\section{实验现象及原始数据记录}` 中的五张原始数据表
- 室温、频率等实验条件
- `\section{数据处理}` 中四种方法对应的计算结果
- “时差法测固体中声速（选做）”部分的结果
- 实验结论、现象分析和讨论题答案

特别注意：

- `speed.tex` 中现在写着一组示例数值，它不会随着 `compute.py` 自动更新
- 你每次更换数据后，都要手动把 `compute.py` 的输出同步到 `speed.tex`

### 3.2 `pic1.png` 的作用

当前 `speed.tex` 在“实验预习”部分直接引用了：

- `Speed/pic1.png`

这张图不是脚本生成的，而是静态示意图。只要文件名和路径不变，LaTeX 编译时就会自动插入。

## 4. 编译 LaTeX 报告

建议在 `Speed` 目录中编译：

```bash
cd /Users/jinana/PHYS1006A/Speed
latexmk -xelatex -interaction=nonstopmode speed.tex
```

编译成功后会生成：

- `Speed/speed.pdf`

如果想清理中间文件，可以运行：

```bash
latexmk -c
```

## 5. 推荐工作流

一次完整实验报告整理，建议按下面流程进行：

1. 在 [compute.py](/Users/jinana/PHYS1006A/Speed/compute.py) 中填入新的 `ROOM_TEMPERATURE_C`、`FREQUENCY_KHZ`、`a`、`b`、`c`、`d`、`e`
2. 运行 `compute.py`，记录理论声速和四种方法的计算结果
3. 在 [speed.tex](/Users/jinana/PHYS1006A/Speed/speed.tex) 中填写原始数据表
4. 用 `compute.py` 的输出替换“数据处理”部分中的示例数值
5. 如果需要完成固体介质部分，再手动补充那一部分的计算
6. 编译 `speed.tex` 生成 PDF

## 6. 常见问题

### 6.1 `numpy` 找不到

说明当前不是在 `tf2` 环境中运行。优先使用：

```bash
conda run --no-capture-output -n tf2 python Speed/compute.py
```

### 6.2 数组长度报错

`compute.py` 中要求 `a`、`b`、`c`、`d`、`e` 都恰好包含 `10` 个数据点，否则会报错。

### 6.3 `speed.tex` 里的结果和脚本输出对不上

这是正常的，因为 `speed.tex` 里的数据处理部分目前只是示例文本，不会自动读取 `compute.py` 的结果。你需要手动同步。

另外，脚本严格按照：

- `ROOM_TEMPERATURE_C`
- `FREQUENCY_KHZ`

这两个常量进行计算。如果你改了室温或频率，最终结果也会随之变化。

### 6.4 想处理“时差法测固体中声速（选做）”

当前 [compute.py](/Users/jinana/PHYS1006A/Speed/compute.py) 没有自动处理这一部分。如果老师要求写这一题，可以：

- 手动在 `speed.tex` 中补算
- 或者后续再扩展脚本
