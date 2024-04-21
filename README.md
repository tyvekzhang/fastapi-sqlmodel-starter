<div  align="center" style="margin-top: 3%">
   <h1>
     FastAPI SQLModel Starter (Fss)
   </h1>
   <p>
     <img src="https://raw.githubusercontent.com/tyvekzhang/fastapi-sqlmodel-starter/main/docs/source/_static/img/fss.svg" alt="logo" style="vertical-align:middle; margin: 0.5%"/>
   </p>
   <p>
     <img alt="GitHub License" src="https://img.shields.io/github/license/tyvekzhang/fastapi-sqlmodel-starter">
     <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastapi-sqlmodel-starter">
     <img alt="CI" src="https://github.com/tyvekzhang/fastapi-sqlmodel-starter/actions/workflows/ci.yaml/badge.svg">
     <img alt="Codecov" src="https://img.shields.io/codecov/c/github/tyvekzhang/fastapi-sqlmodel-starter">
     <img alt="Read the Docs" src="https://img.shields.io/readthedocs/fastapi-sqlmodel-starter">
   </p>
   <h4>
      <p>
        <b>简体中文</b> |
        <a href="https://github.com/tyvekzhang/fastapi-sqlmodel-starter/blob/main/docs/README_en.md">English</a>
     </p>
   </h4>
   <h3>
    PyWeb领域最好用的脚手架之一。
   </h3>
</div>


## 特性

- ⚡ 开箱即用, 实现中间件的零依赖
   - 默认使用Sqlite, 也可自由切换PostgreSQL、MySQL数据库
   - 可选文件或Redis缓存
- 🚢 开启Python代码操作数据库的新体验
- 🚀 简化ORM操作, 内置单表常见操作
- 🎨 丰富的插件机制
   - Jwt安全认证
   - 访问限流
   - Ip黑名单
- 🐋 完备的容器化解决方案
  - Docker
  - Docker-compose
  - Kubernetes
- ✅ 基于GitHub Actions的CI (持续集成) 和 CD (持续交付)

## 文档
- 交互式API文档
  <img alt="API doc"  src="https://raw.githubusercontent.com/tyvekzhang/fastapi-sqlmodel-starter/main/docs/img/api_doc.png">
- 在线文档: [Read the docs](https://fastapi-sqlmodel-starter.readthedocs.io/en/latest/)

## 设置一个conda的虚拟环境
> 这部分是可选的，但可能对新学 Python 的用户有用。

通常来说，在[虚拟环境](https://docs.python.org/3/glossary.html#term-virtual-environment)中安装和运行Python包非常有用，尤其是当你安装了多个版本的Python或使用多个包时。这可以防止升级时出现的问题、不同需求的包之间的冲突、由于有多个Python版本可用而导致的安装问题等等。
管理包和环境的一个选择是使用[conda](https://conda.io/en/latest/)。获取conda的一个快速方式是安装Miniconda：你可以在[这里](https://conda.io/en/latest/miniconda.html)下载它，并在[这里](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation)找到安装说明。例如，在Linux上你会运行：
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
一旦你拥有了conda，你可以创建一个带有Python 3.11(大于等于3.9)的Fss环境
```shell
conda create -n fss_py311 python==3.11 -y
```
然后激活虚拟环境
```shell
conda activate fss_py311
```
## 快速开始
1. 克隆代码
```shell
git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
cd fastapi-sqlmodel-starter
```
2. 安装 Poetry并下载依赖
```shell
conda install poetry -y
poetry install
```
3. 数据库迁移
```shell
cd fss && alembic upgrade head
```
4. 启动
```shell
python apiserver.py
```
5. 交互式文档地址: http://127.0.0.1:9010/docs
6. 恭喜你, 启动成功. 接口访问前需要创建用户, 并进行认证
7. 可以随时按CTRL+C停止运行

## 贡献

欢迎为 FastapiSqlmodelStarter 做出贡献！你可以通过以下方式参与：

- 提交 Bug 或功能需求到 [Issue清单](https://github.com/tyvekzhang/fastapi-sqlmodel-starter/issues)
- 提交代码改进的 Pull Request
- 编写和改进文档
- 分享你使用 FastapiSqlmodelStarter 的经验和想法

## 许可证

FastapiSqlmodelStarter 采用 [MIT 许可证](https://opensource.org/licenses/MIT)开源。
