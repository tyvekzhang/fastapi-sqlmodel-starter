# FastapiSqlmodelStarter (Fss)

Fss aims to be one of the most user-friendly scaffolding tools for PyWeb.

##### 翻译成: [简体中文](../README.md)
## Features

- Out-of-the-box RESTful API support
- Integrated ORM, supporting multiple database backends
- Built-in user authentication and authorization module
- Flexible plugin mechanism for easy expansion
- Built-in security measures to protect against common web attacks
- Excellent performance, suitable for medium to small-sized applications

## Quick Start
1. First, ensure that your Python version is 3.8 or above.
2. Clone the code:
```shell
git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
cd fastapi-sqlmodel-starter
```
3. Create a virtual environment, this example uses venv, similar tools include conda, virtualenv, etc.
```shell
python -m venv env_fss
```
4. Activate the virtual environment:
    - Windows: env_fss\Scripts\activate
    - macOS or Linux: source env_fss/bin/activate
5. Install Poetry and download dependencies:
```shell
pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
poetry install
```
6. Db migration
```shell
alembic upgrade head
```
7. Start the server:
   - Windows: python fss\apiserver.py
   - macOS or Linux: python fss/apiserver.py
8. Access: http://127.0.0.1:9010/docs

## Documentation

## Contribution

We welcome contributions to FastapiSqlmodelStarter! You can participate in the following ways:

- Submit bugs or feature requests to the [Issue Tracker](https://github.com/tyvekzhang/fastapi-sqlmodel-starter/issues)
- Submit Pull Requests for code improvements
- Write and improve documentation
- Share your experiences and ideas using FastapiSqlmodelStarter

## License

FastapiSqlmodelStarter is open-sourced under the [MIT License](https://opensource.org/licenses/MIT).

## Contact Us

- GitHub repository: [https://github.com/tyvekzhang/fastapi-sqlmodel-starter](https://github.com/tyvekzhang/fastapi-sqlmodel-starter)
- Mailing list: [tyvekzhang@gmail.com](mailto:tyvekzhang@gmail.com)

We hope that FastapiSqlmodelStarter will provide convenience and a delightful experience on your journey of Python Web development!
