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
        <b>English</b> |
        <a href="https://github.com/tyvekzhang/fastapi-sqlmodel-starter/blob/main/README.md">简体中文</a>
     </p>
   </h4>
   <h3>
    One of the best scaffolding in the PyWeb field.
   </h3>
</div>

## Features

Here is the translation:

* ⚡ Out-of-the-box, zero-dependency middleware implementation
   - Defaults to SQLite, with flexible switching to PostgreSQL, MySQL databases
   - Optional file or Redis caching
* 🚢 Unlock a new Python coding experience for database operations
* 🚀 Simplify ORM operations, with built-in common single-table operations
* 🎨 Rich plugin mechanism
   - Jwt security authentication
   - Access rate limiting
   - IP blacklisting
* 🐋 Comprehensive containerization solutions
  - Docker
  - Docker-compose
  - Kubernetes
* ✅ Built on GitHub Actions for CI (Continuous Integration) and CD (Continuous Deployment)

## Documentation
- Interactive API documentation
  <img alt="API doc"  src="https://github.com/tyvekzhang/fastapi-sqlmodel-starter/blob/main/docs/img/api_doc.png">
- Online documentation: [Read the docs](https://fastapi-sqlmodel-starter.readthedocs.io/en/latest/)

## Quick Start
1. First, ensure that your Python version is 3.9 or above.
2. Clone the code:
```shell
git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
cd fastapi-sqlmodel-starter/fss
```
3. (Optional)Create a virtual environment, this example uses venv, similar tools include conda, virtualenv, etc.
```shell
python3 -m venv .env_fss
```
4. (Optional)Activate the virtual environment:
    - Windows: .env_fss\Scripts\activate
    - macOS or Linux: source .env_fss/bin/activate
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
   - Windows: python3 apiserver.py
   - macOS or Linux: python3 apiserver.py
8. Access: http://127.0.0.1:9010/docs
9. First, create a new user through the **register** interface, and then proceed with authentication, everything is okay.

## Contribution

We welcome contributions to FastapiSqlmodelStarter! You can participate in the following ways:

- Submit bugs or feature requests to the [Issue Tracker](https://github.com/tyvekzhang/fastapi-sqlmodel-starter/issues)
- Submit Pull Requests for code improvements
- Write and improve documentation
- Share your experiences and ideas using FastapiSqlmodelStarter

## License

FastapiSqlmodelStarter is open-sourced under the [MIT License](https://opensource.org/licenses/MIT).
