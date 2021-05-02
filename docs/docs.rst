.. :tocdepth:: 5

Documentation
=============

Sphinx is included in dev_requirements.txt .
To build the docs run

.. code:: bash

    cd docs
    sphinx-build -b html -E . _build

You can also build the docs by using the Sphinx Makefile as follows

.. code:: bash

    cd docs
    make html

To view the docs, open ``_build/html/index.html`` in your browser