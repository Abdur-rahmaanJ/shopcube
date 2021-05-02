.. :tocdepth:: 2


Modules/Apps
############

Modules allow you to get Django's plug and play behaviour.
The are functionally similar to Django apps. Modules are created
in the modules folder. This makes it easier to comprehend than
Django as you can see at a glance what is the main script and what
are modules/apps.

Easy way to create module
*************************

Once inside a Shopyo project directory (i.e
where the ``app.py`` and ``modules/`` reside), run

.. code:: bash

   shopyo createmodule [OPTIONS] MODULENAME [BOXNAME]

or you can do

.. code:: bash

   python manage.py createmodule [OPTIONS] MODULENAME [BOXNAME]


For example if you run ``shopyo createmodule product``, it will auto create
the following module structure inside ``modules/``

.. code:: none

   .
   └── product/
      ├── static/
      ├── templates/product/
      │   ├── blocks
      │   │   └── sidebar.html
      │   └── dashboard.html
      ├── tests/
      │   ├── test_product_functional.py
      │   └── test_product_models.py
      ├── forms.py
      ├── global.py # optional
      ├── info.json
      ├── models.py
      ├── upload.py # optional
      └── view.py


In case you want to group modules together in a particular subcategory, you can
create modules inside a box. For example first run

.. code:: bash

   shopyo createmodule product box__ecommerce

This will create the box ``box__ecommerce`` if it does not exist and then create the module
``product`` insides it. If now you want another module, for example, ``marketplace`` inside ``box__ecommerce``,
then you can run:

.. code:: bash

   shopyo createmodule marketplace box__ecommerce

With this your modules structure will look like this:


.. code:: none

   .
   └── modules/
       ├── box__ecommerce/
       │   ├── product/
       │   └── marketplace/
       └── ...

You can now acces the ``/product`` and ``/marketplace`` endpoints

See :ref:`createmodule` for more details on command usage. You might find the
EuroPython talk under the `Education Section <education.html>`_ insightful


info.json
*********

The info file allows you to specify module config. This allows you to
specify the module url and panel icon.


.. code:: json

   {
      "author": {
         "mail": "",
         "name": "",
         "website": ""
      },
      "display_string": "Page",
      "module_name":"page",
      "type": "show",
      "fa-icon": "fa fa-store",
      "url_prefix": "/page",
      "dashboard": "/dashboard"
   }

* ``"author``: Metadata to keep track of author of the module. It stores author's ``mail``, ``name``, and ``website`` information
* ``display_string``: Display name on control panel. If you decide to use Shopyo as a Flask base, it does not matter then
* ``module_name``: Shopyo uses this to reference the module. Not to be duplicated
* ``type``: Used to show or hide modules on control panel. If control panel module not present, you can skip it
* ``fa-icon``: Used to show fontawesome icon on control panel. If control panel module not present, you can skip it
* ``url_prefix``: Needed to specify module's base url
* ``dashboard``: Used to redirect in control panel. For example the contact module's url is ``/contact``. But we want it to be public. So we have a panel redirect of ``/dashboard`` to direct admin to ``/contact/dashboard``. Dont include if you don't want redirect

Default Modules/Boxes
*********************
The app comes with the following default modules and boxes

box__bizhelp
------------
* announce
* appoointment
* contact
* page
* people

box__default
------------
* appadmin
* auth
* base
* dashboard
* settings
* theme

www
---

Using Shopyo as a Flask base
****************************

You can customise Shopyo in many ways.
For eample, you can modify exiting modules, add more modules to default boxes
or even remove the modules you do not need. You might however want to keep the following modules:

* appadmin
* auth
* base
* dashboard
* settings


Importing modules
*****************

If you want to import from ``forms.py`` in same folder you write ``from .forms import ...`` . If you want to import from other modules you do: ```from modules.modulename.forms import ...```

global.py
*********

Expects

.. code:: python

    available_everywhere = {

    }


Where you pass functions or vars or classes you want to makle available in all templates! Try 'x': 1

upload.py
*********

``upload.py`` has a ``def upload():`` function where uploads should be done.
This uploads are done when we run ``shopyo initialise``. Example for
uploading an admin user is shown below:

.. literalinclude:: ../shopyo/modules/box__default/auth/upload.py
   :language: python
   :linenos:
