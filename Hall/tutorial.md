# 霍尔效应及其应用

## `hall.tex`, `process.py` 食用说明

本目录包含一份大学物理实验报告 LaTeX 模版，以及与之配套的数据处理与绘图脚本。

目前文件分工如下：

- `hall.tex`：实验报告正文模版
- `process.py`：根据实验数据绘制 5 张曲线图，并输出若干拟合结果
- `vh_im_curve.png`：`V_H-I_M` 曲线图，由 `process.py` 生成
- `vh_is_curve.png`：`V_H-I_S` 曲线图，由 `process.py` 生成
- `b_x_curve.png`：`B-X` 曲线图，由 `process.py` 生成
- `vout_b_curve.png`：`V_{OUT}-B` 曲线图，由 `process.py` 生成
- `vout_theta_curve.png`：`V_{OUT}-\theta` 曲线图，由 `process.py` 生成
- `hall_element.jpg`：讨论题中用到的霍尔元件示意图

建议的使用顺序是：

1. 在 `process.py` 中填入或核对实验数据
2. 运行 `process.py` 生成图像，并记录终端输出的拟合参数
3. 根据图像走势和输出结果整理数据处理结论
4. 将原始数据、分析结论和讨论题答案整理到 `hall.tex`
5. 编译 `hall.tex` 生成实验报告 PDF

## 1. 环境准备

本项目默认使用你已有的 `tf2` conda 环境运行 Python 脚本。

进入项目根目录：

```bash
cd /Users/jinana/PHYS1006A
```

如果要运行 Python 脚本，推荐直接使用：

```bash
conda run --no-capture-output -n tf2 python Hall/process.py
```

如果你已经手动激活了环境，也可以这样运行：

```bash
conda activate tf2
python Hall/process.py
```

## 2. `process.py` 的作用与用法

`process.py` 负责把实验数据绘制成报告里需要插入的 5 张曲线图，并输出线性拟合结果与霍尔元件灵敏度相关计算结果。

### 2.1 需要修改的内容

打开 [process.py](/Users/jinana/PHYS1006A/Hall/process.py)，你会看到目前已经定义好的多组数组：

- `a`、`b`：`V_H-I_M` 数据
- `c`、`d`：`V_H-I_S` 数据
- `e`：用于计算 `K_H` 的磁感应强度数据
- `f`、`g`：`B-X` 数据
- `h`、`i`：`V_{OUT}-B` 数据
- `j`、`k`：`V_{OUT}-\theta` 数据

其中当前各组数据长度分别为：

- `a`、`b`、`c`、`d`、`e`：10 组
- `f`、`g`、`h`、`i`：25 组
- `j`、`k`：19 组

注意：

- 每一组横纵坐标数组长度必须一致
- 改实验数据时，建议保持自变量按大小规律排列，这样图像更直观
- 当前脚本里已经是可运行版本，但如果你替换成自己的数据，后续 `hall.tex` 里的文字结论和数值也要跟着改

### 2.2 当前脚本会生成什么

运行后，`process.py` 会生成以下图片：

- `Hall/vh_im_curve.png`
- `Hall/vh_is_curve.png`
- `Hall/b_x_curve.png`
- `Hall/vout_b_curve.png`
- `Hall/vout_theta_curve.png`

这些图片会被 `hall.tex` 直接引用，所以一般不要改文件名。

同时，脚本还会在终端输出：

- `V_H-I_M` 曲线的斜率和截距
- `V_H-I_S` 曲线的斜率和截距
- `V_{OUT}-B` 在线性范围内 9 个点拟合得到的斜率和截距
- 由 `V_H-I_M` 数据计算出的各组 `K_H`
- 平均霍尔元件灵敏度 `K_H`

也就是说，`process.py` 只负责“算出来并打印出来”，不会自动把这些结果写回 `hall.tex`。

### 2.3 运行方式

在项目根目录运行：

```bash
conda run --no-capture-output -n tf2 python Hall/process.py
```

如果脚本执行成功，终端会显示若干数值，并输出所有图片的保存路径。

## 3. `hall.tex` 的作用与用法

`hall.tex` 是实验报告的主文件。

目前它已经完成了这些工作：

- 设置了报告版式和页眉页脚
- 预留了“实验目的”“实验预习”“实验现象及数据记录”“数据处理及作图”“讨论问题”等部分
- 自动插入 `process.py` 生成的 5 张图
- 插入了讨论题所需的 `hall_element.jpg`
- 给出了数据处理和讨论题的一版示例文字

### 3.1 你通常需要修改哪些部分

建议重点检查和修改：

- 页首的班级、学号、姓名、实验日期
- `\section{实验目的}`、`\section{实验预习}` 的内容
- `\section{实验现象及数据记录}` 中的原始表格
- `\section{数据处理及作图}` 中的公式数值、结论和文字描述
- `\section{讨论问题}` 中的答案表述

特别注意：

- `hall.tex` 里的很多数值目前是手动写进去的，不会随着 `process.py` 自动更新
- 如果你改了 `process.py` 里的实验数据，就要同步修改 `hall.tex` 中这些内容：
  - 线性拟合得到的斜率和截距
  - `K_H` 的计算结果
  - `S_A` 的计算结果
  - 图像走势对应的文字分析

### 3.2 图片如何插入

当前 `hall.tex` 已经写好了以下图片引用：

- `vh_im_curve.png`
- `vh_is_curve.png`
- `b_x_curve.png`
- `vout_b_curve.png`
- `vout_theta_curve.png`
- `hall_element.jpg`

只要这些文件仍在 `Hall` 目录下，LaTeX 编译时就会自动插入。

## 4. 编译 LaTeX 报告

建议在 `Hall` 目录中编译：

```bash
cd /Users/jinana/PHYS1006A/Hall
latexmk -xelatex -interaction=nonstopmode hall.tex
```

编译成功后会生成：

- `Hall/hall.pdf`

如果想清理中间文件，可以运行：

```bash
latexmk -c
```

## 5. 推荐工作流

一次完整实验报告整理，建议按下面流程进行：

1. 在 [process.py](/Users/jinana/PHYS1006A/Hall/process.py) 中更新各组实验数据
2. 运行 `process.py`，确认 5 张图都已正确生成
3. 记录终端输出的斜率、截距、`K_H` 等结果
4. 在 [hall.tex](/Users/jinana/PHYS1006A/Hall/hall.tex) 中同步修改公式里的数值和对应结论
5. 检查图片、图注和讨论题内容是否完整
6. 编译 `hall.tex` 生成 PDF

## 6. 常见问题

### 6.1 `matplotlib` 或 `numpy` 找不到

说明当前不是在 `tf2` 环境中运行。优先使用：

```bash
conda run --no-capture-output -n tf2 python Hall/process.py
```

### 6.2 运行脚本后图片没有更新

优先检查：

- 是否真的运行了 `Hall/process.py`
- 是否在正确目录下查看图片
- 数据数组长度是否匹配

### 6.3 图生成了，但 `hall.tex` 中的数值还是旧的

这是正常现象，因为 `process.py` 不会自动改写 `hall.tex`。需要你把终端输出的结果手动同步到 LaTeX 正文中。

### 6.4 LaTeX 编译失败

优先检查：

- 图片文件是否已经生成
- 图片文件名是否仍为 `vh_im_curve.png`、`vh_is_curve.png`、`b_x_curve.png`、`vout_b_curve.png`、`vout_theta_curve.png`
- `hall_element.jpg` 是否存在
- 是否使用了 `xelatex`

### 6.5 LaTeX 编译出现 Warning，但最终生成了 PDF

如果只是 Warning 且 PDF 已正常输出，一般可以先忽略。优先确认图片、公式和中文显示是否正确即可。
