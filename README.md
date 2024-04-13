<div  align="center" style="margin-top: 3%">
   <h1>
     FastAPI Sqlmodel Starter (Fss)
   </h1>
   <p>
     <img src="https://raw.githubusercontent.com/tyvekzhang/fastapi-sqlmodel-starter/main/docs/img/logo.png" alt="logo" style="vertical-align:middle; margin: 0.5%"/>
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

- 开箱即用, 内置常见数据库、缓存([默认]Sqlite, PostgreSQL, MySQL, [默认]文件缓存, Redis)
- 自带单表的几乎所有操作
- 数据库迁移, 静态代码扫描, 接口文档等一众特性

## 快速开始
1. 首先确保python的版本是3.9及以上的
2. 克隆代码
```shell
git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
cd fastapi-sqlmodel-starter/src
```
3. [可选]创建虚拟环境, 本篇以venv为例, 类似的工具还有conda, virtualenv等
```shell
python3 -m venv .env_fss
```
4. [可选]激活虚拟环境
    - Windows: .env_fss\Scripts\activate
    - macOS 或 Linux: source .env_fss/bin/activate
5. 安装 Poetry并下载依赖
```shell
pip install poetry --trusted-host=mirrors.tuna.tsinghua.edu.cn --index-url=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
poetry install
```
6. 数据库迁移
```shell
alembic upgrade head
```
7. 启动
   - Windows: python3 fss\apiserver.py
   - macOS 或 Linux: python3 fss/apiserver.py
8. 访问: http://127.0.0.1:9010/docs
9. 首先通过注册接口新建用户, 接着进行认证, 一切Ok.
## 文档
- https://fastapi-sqlmodel-starter.readthedocs.io/en/latest/
## 贡献

欢迎为 FastapiSqlmodelStarter 做出贡献！你可以通过以下方式参与：

- 提交 Bug 或功能需求到 [Issue 追踪器](https://github.com/tyvekzhang/fastapi-sqlmodel-starter/issues)
- 提交代码改进的 Pull Request
- 编写和改进文档
- 分享你使用 FastapiSqlmodelStarter 的经验和想法

## 许可证

FastapiSqlmodelStarter 采用 [MIT 许可证](https://opensource.org/licenses/MIT)开源。
