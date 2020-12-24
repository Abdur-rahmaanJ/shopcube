Testing
=========

.. toctree::
    :titlesonly:


run in shopyo/shopyo

.. code:: bash

    python -m pytest .


Alternatively, you can run your tests via `tox <https://tox.readthedocs.io/en/latest/>`_.

run all tests, for all supported Python interpreters

.. code:: bash

    tox


run all tests, on Python 3.8 only

.. code:: bash

    tox -e py38


run all only the `test_home_page` test, on Python 3.9 only

.. code:: bash

    tox -e py39 -- -k test_home_page
