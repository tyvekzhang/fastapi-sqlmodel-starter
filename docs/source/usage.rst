Quick Start
===========

1. First, ensure that your Python version is 3.8 or above.

2. Clone the code::

    git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
    cd fastapi-sqlmodel-starter

3. Create a virtual environment, this example uses venv, similar tools include conda, virtualenv, etc. (Optional)::

    python3 -m venv env_fss

4. Activate the virtual environment: (Optional)

   - Windows::

        env_fss\Scripts\activate

   - macOS or Linux::

        source env_fss/bin/activate

5. Install Poetry and download dependencies::

    pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
    poetry install

6. Database migration::

    alembic upgrade head

7. Start the server:

   - Windows::

        python3 fss\apiserver.py

   - macOS or Linux::

        python3 fss/apiserver.py

8. Access:

   http://127.0.0.1:9010/docs