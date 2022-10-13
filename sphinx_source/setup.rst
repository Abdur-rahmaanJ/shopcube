Setting up Shopyo
=================

Shopyo requires Python. Be sure to have it before!

👟 The easy way
---------------

* [Important] create a virtual environment and activate it.
* install shopyo

.. code-block:: bash

    pip install shopyo

* create new project

* create new shopyo project

.. code-block:: bash

    shopyo new /path/to/location project-name

example

.. code-block:: bash

    shopyo new /home/profiles/arj/desktop shopyotest

* cd into path. if you added path as ``.`` just cd into ``project-name``

* initialise

.. code-block:: bash

    shopyo initialise

* run

.. code-block:: bash

    shopyo runserver

.. note ::

    If the shopyo command is not recognized. close your commandline prompt and reopen


🔧 Install from Github
----------------------

* clone and cd into shopyo/shopyo


.. code-block:: bash

    git clone https://github.com/Abdur-rahmaanJ/shopyo
    cd shopyo/shopyo

* install requirements

.. code-block:: bash

    python -m pip install -r requirements.txt


or if you want to contribute

.. code-block:: bash

    python -m pip install -r dev_requirements.txt


``cd`` into shopyo/shopyo if not done already.

initialise and setup app.

.. code-block:: bash

    python manage.py initialise

run the app.

.. code-block:: bash

    python manage.py runserver

go to the indicated url


**Default Login**
-----------------------

.. code-block:: none

    email: admin@domain.com
    password: pass
