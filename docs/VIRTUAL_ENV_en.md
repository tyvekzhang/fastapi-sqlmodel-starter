# Virtual Environment Setup
Generally speaking, [virtual environments](https://docs.python.org/3/glossary.html#term-virtual-environment) can solve issues such as package conflicts and multiple Python versions. This article provides two methods: Uv、 Conda (Linux).

## 1. Setting up a Virtual Environment with Uv
[uv](https://docs.astral.sh/uv) An extremely fast Python package and project manager, written in Rust.
Install uv with our standalone installers:

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or, from [PyPI](https://pypi.org/project/uv/):

```bash
# With pip.
pip install uv
```

```bash
# Or pipx.
pipx install uv
```

If installed via the standalone installer, uv can update itself to the latest version:

```bash
uv self update
```

See the [installation documentation](https://docs.astral.sh/uv/getting-started/installation/) for
details and alternative installation methods.

## 2. Setting up a Virtual Environment with Conda
[Conda](https://conda.io/en/latest/) is an option for managing packages and environments. You can download Miniconda from [here](https://conda.io/en/latest/miniconda.html).
We'll use **Linux** as an example. For Windows and macOS, please follow the official website instructions for installation.

```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
Create an Fast web virtual environment with Python 3.11 (>=3.9)
```shell
conda create -n fast_web_py311 python==3.11 -y
```
Activate the virtual environment
```shell
conda activate fast_web_py311
```
