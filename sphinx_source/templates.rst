Templating
==========

.. toctree::
    :titlesonly:


Developing a template
---------------------


Please see the `Modules section <modules.html>`_ on how to structure a module.

Having said that, this is the base file we are extending from. 


.. literalinclude:: ../shopyo/modules/box__default/base/templates/base/main_base.html
   :language: html
   :linenos:
   :lines: 1-99


It includes:

* space for user-supplied head (block pagehead)
* space for user-supplied body (block body)
* notification mechanism on the top right

Here is the contact form using the base:

.. literalinclude:: ../shopyo/modules/box__bizhelp/contact/templates/contact/contact_form.html
   :language: html
   :linenos:
   :lines: 1-53


If you extend the base template, you will be able to use the 
notification mechanism used for shopyo api



Global values for templates
---------------------------

Global values for templates can be found in shopyoapi/enhance.py in this function

.. literalinclude:: ../shopyo/shopyoapi/enhance.py
   :language: python
   :linenos:
   :lines: 9-15

Passing parameters to templates
-------------------------------

here is a demo on returning template vars:

.. code:: python

  # 
  # ...
  @module_blueprint.route('/abc')
  def somefunc():
      context = {}
      form = PageForm()

      context.update({
          'form':form,
          'module_name': module_name
      })
      return render_template('page/dashboard.html', **context)

