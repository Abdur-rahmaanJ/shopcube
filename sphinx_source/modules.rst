.. :tocdepth:: 2

============
Modules/Apps
============

Modules allow you to get Django's plug and play behaviour.
The are functionally similar to Django apps. Modules are created
in the modules folder. This makes it easier to comprehend than
Django as you can see at a glance what is the main script and what
are modules/apps.

Easy way to create module
-------------------------

Once in a Shopyo project, run

.. code:: bash

    shopyo startapp modulename

or you can do

.. code:: bash

    python manage.py startapp modulename


What make up modules
--------------------

Modules have the following structure, where product is the module
name. The EuroPython talk under the `Education Section <education.html>`_ might be insightful

.. code:: none

    product/
        tests/
        static/
        templates/
            product/
                templatefile.html
        forms.py
        info.json
        models.py
        view.py
        global.py # optional
        upload.py # optional

The command in the last section auto creates it for you!

info.json
---------

The info file allows you to specify module config. This allows you to
specify the module url and panel icon.


.. code:: json

    {
            "display_string": "Page",
            "module_name":"page",
            "type": "show",
            "fa-icon": "fa fa-store",
            "url_prefix": "/page",
            "dashboard": "/dashboard"
    }

* ``display_string``: Display name on control panel. If you decide to use Shopyo as a Flask base, it does not matter then
* ``module_name``: Shopyo uses this to reference the module. Not to be duplicated
* ``type``: Used to show or hide modules on control panel. If control panel module not present, you can skip it
* ``fa-icon``: Used to show fontawesome icon on control panel. If control panel module not present, you can skip it
* ``url_prefix``: Needed to specify module's base url
* ``dashboard``: Used to redirect in control panel. For example the contact module's url is /contact. But we want it to be public. So we have a panel redirect of /dashboard to direct admin to /contact/dashboard. Dont include if you don't want redirect

Default Modules
----------------

**Admin**

**Appointment**

**Base**

**Category**

**Contact**

**Control Panel**

**Internals**

**Login**

**Page**

**People**

**Setting**

Using Shopyo as a Flask base
----------------------------

You can customise Shopyo in many ways

In case you want a partial customisation, keep the following modules:

* Control Panel
* Admin
* Base
* Login
* Settings

In case you want even more customisation, keep the base module and modify it

If you want even more customisation,  just delete all modules from modules/ folder then run ``shopyo startapp your_module``. In which case, remove models import from shopyoapi/uploads.py


Importing modules
-----------------

If you want to import from forms.py in same folder you write ``from .forms import ...`` . If you want to import from other modules you do: ```from modules.modulename.forms import ...```

global.py
---------


Expects 

.. code:: python

    available_everywhere = {
        
    }


Where you pass functions or vars or classes you want to makle available in all templates! Try 'x': 1

upload.py
---------

upload.py has a def upload(): function where uploads should be done.
put upload codes in the function using app.app_context()

Here is a demo:

.. code::python


    import datetime
    import uuid

    from app import app

    from modules.box__ecommerce.category.models import Category
    from modules.box__ecommerce.category.models import SubCategory
    from modules.box__ecommerce.product.models import Product

    def add_uncategorised_category():
        with app.app_context():
            category = Category(name="uncategorised")
            subcategory = SubCategory(name="uncategorised")
            p1 = Product(
                barcode=str(uuid.uuid1()),
                price=10.0,
                name="Apple",
                in_stock=50,
                selling_price=15.0,
                discontinued=False,
                description="",
            )
            p2 = Product(
                barcode=str(uuid.uuid1()),
                price=10.0,
                name="Pear",
                in_stock=50,
                selling_price=15.0,
                discontinued=False,
                description="",
            )
            p3 = Product(
                barcode=str(uuid.uuid1()),
                price=10.0,
                name="Peach",
                in_stock=50,
                selling_price=15.0,
                discontinued=False,
                description="",
            )

            subcategory.products.extend([p1, p2, p3])
            category.subcategories.append(subcategory)
            category.save()


    def upload():
        print('Adding category and subcategory uncategorised ...')
        add_uncategorised_category()


Boxes or many apps together
---------------------------

If you want to create submodules, first create a box:

.. code:: bash

    python manage.py startbox demo

This will be created as box__demo in modules/

Then create the submodule:

.. code:: bash

    python manage.py startsubapp demoapp in box__demo

If you go to url `/demoapp`, you will get Demoapp returned