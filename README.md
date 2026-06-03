# PHYS1006A

本项目包含了HITSZ “大学物理实验” (PHYS1006A) 课程的 LaTeX 实验报告模板及配套的数据处理 Python 脚本。

## 包含的实验项目

项目中为部分实验单独建立了一个文件夹，通常包含 LaTeX 实验报告模板（`.tex`）、食用说明（`tutorial.md`）以及部分辅助计算与绘图的 Python 脚本。目前库中包含以下实验：

- **Hall/**: 霍尔效应实验
- **Osc/**: 示波器的原理与使用
- **Qss/**: 准稳态法测量比热容
- **RLC/**: RLC 串联谐振电路实验
- **Speed/**: 声速的测量
- **Tension/**: 液体表面张力系数测量
- **Wireless/**: 无线电力传输
- **Wsb/**: 惠斯通电桥测量电阻
- **Young/**: 拉伸法测杨氏弹性模量

## 使用指南

1. **准备工作**: 完成实验后整理好你的原始测量数据。
2. **查阅文档**: 进入对应的实验文件夹，首先阅读 `tutorial.md`（如有）了解具体食用方法和避坑指南，该文档中对表格预留、计算过程都有详细介绍。
3. **数据处理**: 部分实验包含 `process.py`, `compute.py` 或 `drawer.py` 等脚本。可用于辅助进行复杂的逐差法、不确定度计算或绘图处理。
4. **填充模板**: 使用编辑器修改对应的 `.tex` 模板，将其中的示例数据替换为你自己的实测数据。完成误差分析和讨论题。
5. **编译报告**: 报告使用 `ctexart` 文档类，必须使用 XeLaTeX 编译。推荐使用 `latexmk` 命令：

   ```bash
   latexmk -xelatex -interaction=nonstopmode <filename>.tex
   ```

## 环境依赖

- **LaTeX**: 推荐安装 TeX Live 或 MacTeX 等完整发行版，需支持 `xelatex`。
- **Python**: (可选) 如果打算使用 `process.py` / `drawer.py` 等辅助脚本，需要 Python 环境，并可能需要安装 `numpy`、`matplotlib` 等科学计算库。
