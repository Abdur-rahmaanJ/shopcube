Setting up Shopyo
=================

Shopyo requires Python. Be sure to have it before!

👟 The easy way
---------------

* [Important] create a `virtual environment <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_ and activate it
* install shopyo

.. code-block:: bash

   pip install shopyo

* create new project, for example ``blog``

.. code-block:: bash

   mkdir blog
   cd blog

* create new shopyo project for ``blog``

.. code-block:: bash

   shopyo new

See :ref:`new` for more details.

* cd into path of the newly create project.

.. code-block:: bash

   cd blog # path should now /path/to/blog/blog

* initialise

.. code-block:: bash

   shopyo initialise

* run

.. code-block:: bash

   shopyo run

The app should now be running on IP ``127.0.0.1`` at port ``5000``. You can go to http://localhost:5000/ or http://127.0.0.1:5000/. For the home page it will say ``SITE UNDER CONSTRUCTION``.  Go to http://localhost:5000/login/. Login with email ``admin@domain.com`` and password ``pass``

.. note::

   If the shopyo command is not recognized make sure you are in ``blog/blog```
   for this example


🔧 Install from Github
----------------------
See the :ref:`Setup Instructions`