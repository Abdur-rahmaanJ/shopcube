Testing
=========

.. toctree::
    :titlesonly:


For `pytests <https://docs.pytest.org/en/stable/example/simple.html>`__, run all tests inside ``shopyo/shopyo`` directory

.. code:: bash

    # tests with compact output
    python -m pytest .

    # test with verbose output
    python -m pytest -v


Alternatively, you can run your tests via `tox <https://tox.readthedocs.io/en/latest/>`_.

run all tests, for all supported Python interpreters

.. code:: bash

    tox


run all tests, on Python 3.8 only

.. code:: bash

    tox -e py38


run all only the `test_home_page` test, on Python 3.9 only

.. code:: bash

    tox -e py39 -- -k test_shop_home_page
