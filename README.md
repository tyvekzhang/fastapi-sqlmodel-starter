# FastapiSqlmodelStarter (Fss)

![GitHub License](https://img.shields.io/github/license/tyvekzhang/fastapi-sqlmodel-starter)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-sqlmodel-starter)
![CI](https://img.shields.io/github/actions/workflow/status/tyvekzhang/fastapi-sqlmodel-starter/ci.yaml)
![Codecov (with branch)](https://img.shields.io/codecov/c/github/tyvekzhang/fastapi-sqlmodel-starter/dev)
![Read the Docs](https://img.shields.io/readthedocs/fastapi-sqlmodel-starter)

Fss旨在成为PyWeb中对用户最友好的脚手架工具之一。

##### Translate to: [English](docs/README_en.md)
## 特性

- 开箱即用, 内置常见数据库、缓存(Sqlite[默认], PostgreSQL, MySQL, 文件缓存[默认], Redis)
- 自带单表的几乎所有操作
- 数据库迁移, 静态代码扫描, 接口文档等一众特性

## 快速开始
1. 首先确保python的版本是3.8及以上的
2. 克隆代码
```shell
git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
cd fastapi-sqlmodel-starter
```
3. 创建虚拟环境, 本篇以venv为例, 类似的工具还有conda, virtualenv等(可选)
```shell
python3 -m venv .env_fss
```
4. 激活虚拟环境(可选)
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

## 联系我们

- GitHub 仓库：[https://github.com/tyvekzhang/fastapi-sqlmodel-starter](https://github.com/tyvekzhang/fastapi-sqlmodel-starter)
- 邮件列表：[tyvekzhang@gmail.com](mailto:tyvekzhang@gmail.com)


希望 FastapiSqlmodelStarter 能为你的 Python Web 开发之旅提供便利和愉悦的体验！
