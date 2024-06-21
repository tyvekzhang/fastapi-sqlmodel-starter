# 虚拟环境设置
通常来说, [虚拟环境](https://docs.python.org/3/glossary.html#term-virtual-environment)可以解决包冲突和多版本Python等问题. 本篇给出了Conda(Linux), Venv(Windows)两种方法

## 1. Conda设置虚拟环境
[conda](https://conda.io/en/latest/)是管理包和环境的一种选择. 可以从[这里](https://conda.io/en/latest/miniconda.html)下载Miniconda,
我们就以**Linux**为例, Windows, macOS请按照官网说明进行安装.

```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
设置镜像源
```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```
创建带有Python 3.11(>=3.9)的Fss虚拟环境
```shell
conda create -n fss_py311 python==3.11 -y
```
激活虚拟环境
```shell
conda activate fss_py311
```

## 2. Venv设置虚拟环境
使用[venv](https://docs.python.org/3/library/venv.html)之前, 请确保[python](https://www.python.org/downloads/)的版本>=3.9, 我们就以**Windows**为例, Linux, macOS请按照官网说明进行安装.
创建名为.fss_py311的虚拟环境
```shell
python -m venv .fss_py311
```
激活虚拟环境
1. cmd.exe
```shell
.fss_py311\Scripts\activate.bat
```

2. PowerShell
```shell
.fss_py311\Scripts\Activate.ps1
```

配置镜像源
```shell
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```
