.. :tocdepth:: 5

Contributing to Shopyo
======================


Shopyo is built using Flask but mimicks Django so that you get to use plug and play modules,
to contribute, it's nice to know Flask well. Here are some resources which might help you:

Resources
----------

Please see the `Education <education.html>`_ section to see what you need to learn before contributing.


Github instructions
-------------------

If you want to contribute, go ahead, we ❤️ it. We follow a 💯 % first-timers-friendly policy.

* Fork repo.
* Create a new branch. For example: ``bg-fix-migration-file``.
* Once you have add your changes ensure tests are still passing.
* Add tests for any new functionality added.
* Ensure you commits follow the standard specified `here <https://udacity.github.io/git-styleguide/>`_.
* Follow the Pull request template.
* Add your country flag in readme after accepted PR

* Follow :ref:`Update fork` then
* Push ``git push origin <branch-name>``
* If it closes an issue, add ``Fixes #94`` for example, as seen `here <https://github.com/Abdur-rahmaanJ/shopyo/pull/95>`_
*  PR against ``dev`` branch, not master

Update Fork
-----------

.. code:: bash

    cd <your/local/cloned/repo/path/here>
    git remote add upstream https://github.com/Abdur-rahmaanJ/shopyo.git
    git fetch upstream
    git pull upstream master



Contributing to package
-----------------------

* clone project
* cd into project folder
* create and activate venv
* run ``pip install -e .``
* after changes run ``pip install -e . --upgrade``
* test ``shopyo <your options>``

Maintainers notes
-----------------

* Version is found in shopyo/__init__.py

.. literalinclude:: ../shopyo/__init__.py
   :language: python
   :linenos:
   :lines: 2-3

* to publish to pypi, run

.. code:: bash

    python setup.py publish

💬 Community: Discord
---------------------
 Join the Discord community `Discord Group <https://discord.gg/k37Ef6w/>`_

