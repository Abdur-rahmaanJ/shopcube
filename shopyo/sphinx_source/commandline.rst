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

   .. code:: bash

      shopyo new blog
      cd blog
      python -m pip install -r requirements.txt
      cd blog
      python manage.py initialise
      python manage.py rundebug

Complete commands
-----------------

**Db from scratch**

.. code:: bash

   python manage.py db init # create db from new


**Migrate**

.. code-block:: bash


   python manage.py db migrate
   python manage.py db upgrade

**Clean**

.. code-block:: bash

   python manage.py clean

removes ``__pycache__/``, ``shopyo.db`` and ``migrations``.

**Initialise**

.. code-block:: bash

   shopyo initialise


**Run server**


.. code-block:: bash

   python manage.py runserver


**Collect static**


.. code-block:: bash

   python manage.py collectstatic

.. code-block:: bash

   python manage.py collectstatic demoapp


.. code-block:: bash

   python manage.py collectstatic box__somebox/demoapp