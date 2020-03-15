Templating
==========

.. toctree::
    :titlesonly:


Developing a template.
-------------------------------------


Each landing page and subsection should contain the following headers.

.. literalinclude:: ../shopyo/modules/admin/templates/admin/index.html
   :language: python
   :linenos:
   :lines: 1-3

This extends the base.html file and
sets the active section (change section name).


Create the main landing page of a new section in the template folder.

Inside the modules template folder create a folder named as you want::

    modules
    /section_name
        /templates
            /section_name
                index.html

**Create a subsection template**.


Inside the module section template folder create a new file under the folder named same as the section::

    modules
        /section_name
            /templates
                /section_name
                    index.html``

**Create navigation elements for a new section.**
Inside the template folder create a file named ``nav.html``::

    /modules
        /section_name
            /templates
                /section_name
                    index.html
                    nav.html

In the  ``nav.html``  file elements for the navigation can be created.

**To display the navagation elements.**

Open the modules ``/base`` folder and locate the ``nav_base.html``.

In the ``nav_bar_log([])`` array. Enter the section name last in the list

.. literalinclude:: ../shopyo/modules/base/templates/base/nav_base.html
   :language: python
   :linenos:
   :lines: 1-10


Now enter a new ``elif`` statement containing a reference
to the ``nav_base.html``

.. literalinclude:: ../shopyo/modules/base/templates/base/nav_base.html
   :language: python
   :linenos:
   :lines: 25-50

Then the navagation elements will be displayed in the new section.
