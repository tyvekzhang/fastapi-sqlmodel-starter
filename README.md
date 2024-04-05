# FastapiSqlmodelStarter(Fss)

FastapiSqlmodelStarter旨在成为搭建Python Web领域的小而美的工具。

##### Translate to: [English](docs/README_en.md)
## 特性

- 开箱即用的 RESTful API 支持
- 集成 ORM，支持多种数据库后端
- 内置用户认证和授权模块
- 灵活的插件机制，易于扩展
- 内置安全防护，抵御常见 Web 攻击
- 优秀的性能表现，适合中小型应用

## 快速开始
1. 首先确保python的版本是3.8及以上的
2. 克隆代码
```shell
git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
cd fastapi-sqlmodel-starter
```
3. 创建虚拟环境, 本篇以venv为例, 类似的工具还有conda, virtualenv等
```shell
python -m venv env_fss
```
2. 激活虚拟环境
    - Windows: env_fss\Scripts\activate
    - macOS 或 Linux: source env_fss/bin/activate
3. 安装 Poetry并下载依赖
```shell
pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
poetry install
```
4. 启动
   - Windows: python fss\apiserver.py
   - macOS 或 Linux: python fss/apiserver.py
5. 访问: http://127.0.0.1:9010/docs
## 文档

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
