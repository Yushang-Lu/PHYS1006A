# 磁耦合共振式无线电力传输实验

## `wireless.tex`, `drawer.py` 食用说明

本目录包含一份大学物理实验报告 LaTeX 模版，以及与之配套的绘图脚本。

目前文件分工如下：

- `wireless.tex`：实验报告正文模版
- `drawer.py`：根据实验数据绘制两张曲线图
- `graph1.png`：幅度-频率曲线图，由 `drawer.py` 生成
- `graph2.png`：灯泡电压-距离曲线图，由 `drawer.py` 生成

建议的使用顺序是：

1. 在 `drawer.py` 中填入实验数据
2. 运行 `drawer.py` 生成两张图
3. 根据图像总结峰值位置和曲线规律
4. 将原始数据、分析结论和讨论题答案整理到 `wireless.tex`
5. 编译 `wireless.tex` 生成实验报告 PDF

## 1. 环境准备

本项目默认使用你已有的 `tf2` conda 环境运行 Python 脚本。

进入项目根目录：

```bash
cd /Users/jinana/PHYS1006A
```

如果要运行 Python 脚本，推荐直接使用：

```bash
conda run --no-capture-output -n tf2 python Wireless/drawer.py
```

如果你已经手动激活了环境，也可以这样运行：

```bash
conda activate tf2
python Wireless/drawer.py
```

## 2. `drawer.py` 的作用与用法

`drawer.py` 负责把实验数据绘制成报告里需要插入的两张曲线图。

### 2.1 需要修改的内容

打开 [drawer.py](/Users/jinana/PHYS1006A/Wireless/drawer.py)，修改以下四项：

- `a = [...]`
- `b = [...]`
- `c = [...]`
- `d = [...]`

其中：

- `a` 表示研究振荡频率影响时记录的频率数据，单位是 `kHz`
- `b` 表示与 `a` 对应的灯泡电压数据，单位是 `V`
- `c` 表示研究传输距离影响时记录的距离数据，单位是 `cm`
- `d` 表示与 `c` 对应的灯泡电压数据，单位是 `V`

注意：

- `a` 和 `b` 的长度必须一致
- `c` 和 `d` 的长度必须一致
- `a`、`c` 最好按从小到大排列，这样图像更直观
- 当前脚本里给的是一组示例数据，正式写报告前建议替换成自己的实测值

### 2.2 峰值标注和坐标范围

脚本会自动用：

```python
peak_index = int(np.argmax(y))
```

寻找纵坐标最大值所在的数据点。

但是需要特别注意，图上的说明文字目前是写死的，例如：

```python
"Peak\n(2260 kHz, 16.50 V)"
"Peak\n(19 cm, 18.30 V)"
```

如果你换了实验数据，峰值位置发生变化，建议同步检查并修改：

- 两处 `ax.annotate(...)` 里的文字内容
- `xytext=(...)` 的文字摆放位置
- `ax.set_xlim(...)` 和 `ax.set_ylim(...)` 的显示范围

否则虽然脚本仍能运行，但图上标注文字可能和真实峰值不一致，或者标注框跑到不合适的位置。

### 2.3 输出文件

运行后会在 `Wireless` 目录下生成两张图片：

- `Wireless/graph1.png`
- `Wireless/graph2.png`

它们分别对应：

- 幅度-频率曲线
- 灯泡电压-距离曲线

这些图片会被 `wireless.tex` 直接引用，所以一般不要改文件名。

### 2.4 运行方式

在项目根目录运行：

```bash
conda run --no-capture-output -n tf2 python Wireless/drawer.py
```

## 3. `wireless.tex` 的作用与用法

`wireless.tex` 是实验报告的主文件。

目前它已经完成了这些工作：

- 设置了报告版式和页眉页脚
- 预留了“实验预习指导”“原始数据记录”“数据处理”“讨论题”等部分
- 自动插入 `drawer.py` 生成的两张图
- 给出了数据处理、现象分析和讨论题的一版示例文字

### 3.1 你通常需要修改哪些部分

建议重点检查和修改：

- 页首的班级、学号、姓名、实验日期
- `\section{原始数据记录}` 的内容
- `\section{数据处理}` 中的峰值位置、峰值电压和曲线规律描述
- “自制无线电力传输系统”部分的实际传输效果和误差分析
- 讨论题答案

特别注意：

- `wireless.tex` 里的数值描述目前和 `drawer.py` 里的示例数据一致
- 如果你替换了实验数据，就要手动把文字中的峰值位置和结论一起改掉

### 3.2 图片如何插入

当前 `wireless.tex` 已经写好了图片引用：

- `graph1.png`
- `graph2.png`

只要 `drawer.py` 已经生成这两张图，并且文件仍在 `Wireless` 目录下，LaTeX 编译时就会自动插入。

## 4. 编译 LaTeX 报告

建议在 `Wireless` 目录中编译：

```bash
cd /Users/jinana/PHYS1006A/Wireless
latexmk -xelatex -interaction=nonstopmode wireless.tex
```

编译成功后会生成：

- `Wireless/wireless.pdf`

如果想清理中间文件，可以运行：

```bash
latexmk -c
```

## 5. 推荐工作流

一次完整实验报告整理，建议按下面流程进行：

1. 在 [drawer.py](/Users/jinana/PHYS1006A/Wireless/drawer.py) 中填入新的 `a`、`b`、`c`、`d`
2. 运行 `drawer.py`，检查两张图是否正常
3. 如果峰值标注、坐标范围或文字位置不合适，就在 `drawer.py` 中继续微调后重新生成图片
4. 在 [wireless.tex](/Users/jinana/PHYS1006A/Wireless/wireless.tex) 中更新原始数据、图像分析和结论
5. 编译 `wireless.tex` 生成 PDF

## 6. 常见问题

### 6.1 `matplotlib` 或 `numpy` 找不到

说明当前不是在 `tf2` 环境中运行。优先使用：

```bash
conda run --no-capture-output -n tf2 python Wireless/drawer.py
```

### 6.2 图上的峰值标注和数据不一致

这通常不是绘图失败，而是因为 `ax.annotate(...)` 里的说明文字写死了。换了数据后，记得一起修改峰值文字。

### 6.3 图像被截断，或者峰值点看起来挤在边缘

优先检查：

- `ax.set_xlim(...)`
- `ax.set_ylim(...)`
- `xytext=(...)`

如果你的数据范围和当前示例差很多，这三处通常都需要一起调整。

### 6.4 LaTeX 编译失败

优先检查：

- 图片文件是否已经生成
- 图片文件名是否仍为 `graph1.png`、`graph2.png`
- 是否使用了 `xelatex`
