Quick Start
===========

.. _setting-up-a-conda-virtual-environment:

Setting up a Conda Virtual Environment
---------------------------------------

.. note::
This part is optional, but may be useful for new Python learners.

Typically, it's beneficial to install and run Python packages in a `virtual environment`_, especially when you have multiple versions of Python or use multiple packages. This can prevent issues during upgrades, conflicts between packages with different requirements, and installation problems due to multiple Python versions.

One choice for managing packages and environments is `conda`_. A quick way to get conda is to install Miniconda: you can download it from `here`_ and find installation instructions `here`_. For example, on Linux, you would run:

.. code-block:: shell

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh

Once you have conda, you can create an FSS environment with Python 3.11 (or greater than 3.9):

.. code-block:: shell

    conda create -n fss_py311 python==3.11 -y
    conda activate fss_py311

.. _Quick Start:

Quick Start
------------

1. **Clone the code**:

.. code-block:: shell

    git clone https://github.com/tyvekzhang/fastapi-sqlmodel-starter
    cd fastapi-sqlmodel-starter

2. **Install Poetry and download dependencies with conda**:

.. code-block:: shell

    conda install poetry -y
    poetry install
3. **Or install Poetry and download dependencies via pip**:

.. code-block:: shell

    pip install poetry
    poetry install

3. **Database migration**:

.. code-block:: shell

    cd fss && alembic upgrade head

4. **Start the server**:

.. code-block:: shell

    python apiserver.py

5. **Interactive documentation address**: http://127.0.0.1:9010/docs

6. Congratulations, you've successfully started the server! You need to create a user and authenticate before accessing the API.

7. **Stop the server**: You can stop the server at any time by pressing CTRL+C.

.. _virtual environment: https://docs.python.org/3/glossary.html#term-virtual-environment
.. _conda: https://conda.io/en/latest/
.. _here: https://conda.io/en/latest/miniconda.html
.. _here: https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation
