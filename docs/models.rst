======
Models
======

.. toctree::
    :titlesonly:

Creating a model
----------------
.. literalinclude:: ../shopyo/modules/admin/models.py
   :language: python
   :linenos:
   :lines: 13-25

🔩 Migrations
-------------

In case of change to models, do

.. code-block:: python
   :caption: Updating the database.
   :name: migrations

   python manage.py db migrate
   python manage.py db upgrade

Complete commands

.. code-block:: python
   :caption: Initialise database from scratch.
   :name: migrations_2

   python manage.py db init # create db from new
   python manage.py db migrate
   python manage.py db upgrade

.. code-block:: python
   :caption: Clean project
   :name: migrations_3

   python manage.py clean

removes ``__pycache__/``, ``test.db`` and ``migrations``.
