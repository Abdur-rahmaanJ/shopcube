.. :tocdepth:: 5

Assets Management
=================


.. code:: python

   from shopyo.api.assets import get_static


In the case of a module in box:


.. code:: python

   @module_blueprint.route('/img_test')
   def img_test_box():
       return '<img src="{}">'.format(get_static('box__qwerty/modulez', 'shop.png'))


In the case of a module outside box


.. code:: python

   @module_blueprint.route('/img_test2')
   def img_test_module():
       return '<img src="{}">'.format(get_static('modulez', 'shop.png'))


If DEBUG True, it will be served from the module's static folder.

If DEBUG False, it will be served from main static folder. Make sure to run

.. code:: bash

   python manage.py collectstatic

before

You can test the difference by running 

.. code:: bash

   shopyo run --debugger

and 

.. code:: bash

   shopyo run --no-debugger


Your code remains the same. Just the location changes.


Just if using apache, alias /static to server from main static folder