Commandline Args
================

.. toctree::
    :titlesonly:

Various commandline args exist to ease your life. The initialise command for example
is a combination of many commands


.. note::

   You can run

   .. code:: bash

       shopyo <command>

   or

   .. code:: bash

       python manage.py <command>

    except for the ``shopyo new ...``` command

Complete commands
-----------------

**Db from scratch**

.. code:: bash

   shopyo db init # create db from new


**Migrate**

.. code-block:: bash


   shopyo db migrate
   shopyo db upgrade

**Clean**

.. code-block:: bash

   shopyo clean

removes ``__pycache__/``, ``shopyo.db`` and ``migrations``.

**Initialise**

.. code-block:: bash

   shopyo initialise


**Run server**


.. code-block:: bash

   shopyo runserver