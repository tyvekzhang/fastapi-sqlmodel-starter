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
    Fss aims to be one of the best scaffold in PyWeb.
   </h3>
</div>

## Features

Here is the translation:

* ⚡ Out-of-the-box, zero-dependency middleware implementation
   - Defaults to SQLite, with flexible switching to PostgreSQL, MySQL databases
   - Optional file or Redis caching
* 🚢 Unlock a new Python coding experience for database table operations
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
  <img alt="API doc"  src="https://raw.githubusercontent.com/tyvekzhang/fastapi-sqlmodel-starter/main/docs/img/api_doc.png">
- Online documentation: [Read the docs](https://fastapi-sqlmodel-starter.readthedocs.io/en/latest/)

## Setting up a Conda Virtual Environment
> This part is optional, but may be useful for new Python learners.

Here is the translation of the given text to English:

Typically, [virtual environments](https://docs.python.org/3/glossary.html#term-virtual-environment) can solve issues like package conflicts and multiple versions of Python. [Conda](https://conda.io/en/latest/) is a choice for managing packages and environments. On Linux, you can download Miniconda from [here](https://conda.io/en/latest/miniconda.html) and follow the instructions for installation.
```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
Once you have conda, you can create an FSS environment with Python 3.11 (or greater than 3.9)
```shell
conda create -n fss_py311 python==3.11 -y
```
Then activate the virtual environment
```shell
conda activate fss_py311
```
## Quick Start
1. Clone the code
```shell
git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
cd fastapi-sqlmodel-starter
```
2. Install Poetry and download dependencies with conda
```shell
conda install poetry -y
poetry install
```
3. Or install poetry and download dependencies with pip
```shell
pip install poetry
poetry install
```
4. Database migration
```shell
cd fss && alembic upgrade head
```
5. Start the server
```shell
python apiserver.py
```
6. Interactive documentation address: http://127.0.0.1:9010/docs
7. Congratulations, you've successfully started the server! You need to create a user and authenticate before
   accessing the API.
8. You can stop the server at any time by pressing CTRL+C.

## Contribution

We welcome contributions to FastapiSqlmodelStarter! You can participate in the following ways:

- Submit bugs or feature requests to the [Issue Tracker](https://github.com/tyvekzhang/fastapi-sqlmodel-starter/issues)
- Submit Pull Requests for code improvements
- Write and improve documentation
- Share your experiences and ideas using FastapiSqlmodelStarter

## License

FastapiSqlmodelStarter is open-sourced under the [MIT License](https://opensource.org/licenses/MIT).
