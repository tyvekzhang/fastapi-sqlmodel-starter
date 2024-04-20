Quick Start
===========

1. First, ensure that your Python version is 3.9 or above.

2. Clone the code::

    git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
    cd fastapi-sqlmodel-starter/fss

3. (Optional)Create a virtual environment, this example uses venv, similar tools include conda, virtualenv, etc:

    python3 -m venv .env_fss

4. (Optional)Activate the virtual environment:

   - Windows::

        .env_fss\Scripts\activate

   - macOS or Linux::

        source .env_fss/bin/activate

5. Install Poetry and download dependencies::

    pip install poetry
    poetry install

6. Database migration::

    alembic upgrade head

7. Start the server:

   - Windows::

        python3 apiserver.py

   - macOS or Linux::

        python3 apiserver.py

8. Access:

   http://127.0.0.1:9010/docs

9. First, create a new user through the register interface. Then, proceed with authentication.
