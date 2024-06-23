# Virtual Environment Setup
Generally speaking, [virtual environments](https://docs.python.org/3/glossary.html#term-virtual-environment) can solve issues such as package conflicts and multiple Python versions. This article provides two methods: Conda (Linux) and Venv (Windows).

## 1. Setting up a Virtual Environment with Conda
[Conda](https://conda.io/en/latest/) is an option for managing packages and environments. You can download Miniconda from [here](https://conda.io/en/latest/miniconda.html).
We'll use **Linux** as an example. For Windows and macOS, please follow the official website instructions for installation.

```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
Create an Fss virtual environment with Python 3.11 (>=3.9)
```shell
conda create -n fss_py311 python==3.11 -y
```
Activate the virtual environment
```shell
conda activate fss_py311
```

## 2. Setting up a Virtual Environment with Venv
Before using [venv](https://docs.python.org/3/library/venv.html), please ensure that your [Python](https://www.python.org/downloads/) version is >=3.9. We'll use **Windows** as an example. For Linux and macOS, please follow the official website instructions for installation.
Create a virtual environment named .fss_py311
```shell
python -m venv .fss_py311
```
Activate the virtual environment
1. cmd.exe
```shell
.fss_py311\Scripts\activate.bat
```

2. PowerShell
```shell
.fss_py311\Scripts\Activate.ps1
```
