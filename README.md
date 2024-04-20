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

## 快速开始
1. 首先确保python版本为3.9及以上
2. 克隆代码
```shell
git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
cd fastapi-sqlmodel-starter/fss
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
   - Windows: python3 apiserver.py
   - macOS 或 Linux: python3 apiserver.py
8. 访问: http://127.0.0.1:9010/docs
> 成功访问后需要创建用户并认证

## 贡献

欢迎为 FastapiSqlmodelStarter 做出贡献！你可以通过以下方式参与：

- 提交 Bug 或功能需求到 [Issue清单](https://github.com/tyvekzhang/fastapi-sqlmodel-starter/issues)
- 提交代码改进的 Pull Request
- 编写和改进文档
- 分享你使用 FastapiSqlmodelStarter 的经验和想法

## 许可证

FastapiSqlmodelStarter 采用 [MIT 许可证](https://opensource.org/licenses/MIT)开源。
