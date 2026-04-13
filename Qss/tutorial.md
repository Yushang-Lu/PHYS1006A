# 准稳态法测不良导体的比热容和导热系数

## `qss.tex`, `drawer.py`, `process.py` 食用说明

本目录包含一份大学物理实验报告 LaTeX 模版，以及与之配套的绘图、数据处理脚本。

目前文件分工如下：

- `qss.tex`：实验报告正文模版
- `drawer.py`：将热电偶原始数据换算成温升，并绘制三张折线图
- `process.py`：在准稳态区间内用最小二乘法计算 `\Delta T` 和 `dT/d\tau`

建议的使用顺序是：

1. 在 `drawer.py` 中填入实验数据
2. 运行 `drawer.py` 生成三张图
3. 根据图像确定准稳态区间
4. 在 `process.py` 中设置准稳态区间并运行计算
5. 将结果整理到 `qss.tex`
6. 编译 `qss.tex` 生成实验报告 PDF

## 1. 环境准备

本项目默认使用你已有的 `tf2` conda 环境运行 Python 脚本。

进入项目根目录：

```bash
cd /Users/jinana/PHYS1006A
```

如果要运行 Python 脚本，推荐直接使用：

```bash
conda run --no-capture-output -n tf2 python Qss/drawer.py
conda run --no-capture-output -n tf2 python Qss/process.py
```

如果你已经手动激活了环境，也可以这样运行：

```bash
conda activate tf2
python Qss/drawer.py
python Qss/process.py
```

## 2. `drawer.py` 的作用与用法

`drawer.py` 负责把热电偶电势数据换算成温升，并生成报告中要插入的图片。

### 2.1 需要修改的内容

打开 [drawer.py](/Users/jinana/PHYS1006A/Qss/drawer.py)，修改以下三项：

- `a = [...]`
- `b = [...]`
- `k = 40`

其中：

- `a` 表示加热面热电偶电势，单位是 `μV`
- `b` 表示中心面热电偶电势，单位是 `μV`
- `k` 表示热电偶比例系数，当前代码中采用 `40 μV/K`

注意：

- `a` 和 `b` 都必须正好有 `30` 个数
- 每个数之间用逗号分隔
- 支持整数和小数

### 2.2 数据的物理意义

脚本中按下面的方式换算：

```python
c = a / k
d = b / k
```

这里得到的 `c`、`d` 不是绝对温度，而是：

- 加热面相对参考端的温升
- 中心面相对参考端的温升

而：

```python
diff = c - d
```

表示样品内部两测点的温差，也就是 `\Delta T`。

### 2.3 运行方式

在项目根目录运行：

```bash
conda run --no-capture-output -n tf2 python Qss/drawer.py
```

### 2.4 输出文件

运行后会在 `Qss` 目录下生成三张图片：

- `Qss/heat_curve.png`
- `Qss/central_curve.png`
- `Qss/heat_minus_central_curve.png`

它们分别对应：

- 加热面相对参考端温升随时间变化曲线
- 中心面相对参考端温升随时间变化曲线
- `\Delta T-\tau` 曲线

这些图片会被 `qss.tex` 直接引用，所以一般不要改文件名。

## 3. `process.py` 的作用与用法

`process.py` 负责在准稳态区间内计算：

- `\Delta T`
- `dT/d\tau`

它会直接从 [drawer.py](/Users/jinana/PHYS1006A/Qss/drawer.py) 导入 `a`、`b`、`k`，所以通常只需要维护一份原始数据。

### 3.1 计算方法

当前脚本采用以下方法：

1. 由 `a`、`b`、`k` 计算 `c = a / k`、`d = b / k`
2. 选取准稳态区间
3. 只使用准稳态区间内的数据点
4. 分别对 `c-\tau` 和 `d-\tau` 做最小二乘直线拟合
5. 取两条拟合直线斜率的平均值作为 `dT/d\tau`
6. 取同一区间内 `(c-d)` 的平均值作为 `\Delta T`

### 3.2 准稳态区间如何设置

打开 [process.py](/Users/jinana/PHYS1006A/Qss/process.py)，修改：

```python
QUASI_STEADY_START = 7
QUASI_STEADY_END = 14
```

这两个数表示参与拟合的数据下标区间，对应时间区间 `\tau = 7~14 min`。

建议先看 `drawer.py` 生成的三张图，再决定是否修改这两个值。

判断进入准稳态的经验标准是：

- 加热面与中心面的 `T-\tau` 曲线近似为两条平行直线
- `\Delta T-\tau` 曲线基本保持稳定

### 3.3 运行方式

```bash
conda run --no-capture-output -n tf2 python Qss/process.py
```

### 3.4 输出内容

运行后终端会输出：

- 当前采用的计算方法说明
- 实际参与拟合的 `tau`、`c`、`d` 数据点
- 加热面和中心面拟合直线的斜率、截距、`R^2`
- 最终的 `\Delta T` 和 `dT/d\tau`

这些结果可以直接整理到 [qss.tex](/Users/jinana/PHYS1006A/Qss/qss.tex) 的“数据处理”部分。

## 4. `qss.tex` 的作用与用法

`qss.tex` 是实验报告的主文件。

目前它已经完成了这些工作：

- 设置了报告版式和页眉页脚
- 预留了“原始数据记录”“数据处理”“实验现象分析及结论”“讨论题”等部分
- 自动插入 `drawer.py` 生成的三张图

### 4.1 你通常需要修改哪些部分

建议重点检查和修改：

- 页首的班级、学号、姓名、实验日期
- `\section{原始数据记录}` 的内容
- `\section*{三、数据处理}` 中的文字说明与公式
- 由 `process.py` 计算得到的 `\Delta T` 和 `dT/d\tau`
- 导热系数 `\lambda` 和比热容 `c` 的最终计算值
- 讨论题回答

### 4.2 图片如何插入

当前 `qss.tex` 已经写好了图片引用：

- 前两张图水平并排显示
- 第三张图单独显示

只要 `drawer.py` 已经生成：

- `heat_curve.png`
- `central_curve.png`
- `heat_minus_central_curve.png`

并且文件仍在 `Qss` 目录下，LaTeX 编译时就会自动插入它们。

## 5. 编译 LaTeX 报告

建议在 `Qss` 目录中编译：

```bash
cd /Users/jinana/PHYS1006A/Qss
latexmk -xelatex -interaction=nonstopmode qss.tex
```

编译成功后会生成：

- `Qss/qss.pdf`

如果想清理中间文件，可以运行：

```bash
latexmk -c
```

## 6. 推荐工作流

一次完整实验报告整理，建议按下面流程进行：

1. 在 [drawer.py](/Users/jinana/PHYS1006A/Qss/drawer.py) 中填入新的 `a`、`b`、`k`
2. 运行 `drawer.py`，检查三张图是否正常
3. 根据图像判断准稳态区间
4. 在 [process.py](/Users/jinana/PHYS1006A/Qss/process.py) 中修改 `QUASI_STEADY_START` 和 `QUASI_STEADY_END`
5. 运行 `process.py`，记录 `\Delta T` 和 `dT/d\tau`
6. 在 [qss.tex](/Users/jinana/PHYS1006A/Qss/qss.tex) 中更新文字、公式和结论
7. 编译 `qss.tex` 生成 PDF

## 7. 常见问题

### 7.1 `matplotlib` 或 `numpy` 找不到

说明当前不是在 `tf2` 环境中运行。优先使用：

```bash
conda run --no-capture-output -n tf2 python Qss/drawer.py
conda run --no-capture-output -n tf2 python Qss/process.py
```

### 7.2 `a` 或 `b` 报长度错误

`drawer.py` 中要求 `a` 和 `b` 必须都恰好包含 `30` 个数据点，否则会报错。

### 7.3 LaTeX 编译失败

优先检查：

- 图片文件是否已经生成
- 图片文件名是否仍为 `heat_curve.png`、`central_curve.png`、`heat_minus_central_curve.png`
- 是否使用了 `xelatex`

推荐编译命令：

```bash
latexmk -xelatex -interaction=nonstopmode qss.tex
```

如果出现中文字体相关报错，一般需要检查本机 TeX 环境和中文字体配置。

## 8. 当前模板中的默认结论

以当前仓库中的示例数据为例，脚本给出的结果大致为：

- 准稳态区间：`\tau = 7~14 min`
- `\Delta T \approx 2.00 K`
- `dT/d\tau \approx 0.526 K/min`

这些值只是当前示例数据对应的结果。你换成自己的实验数据后，应重新运行 `drawer.py` 和 `process.py`，不要直接照抄旧结果。
