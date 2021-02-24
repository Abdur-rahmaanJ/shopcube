.. :tocdepth:: 5

Contributing to Shopyo
======================


Shopyo is built using Flask but mimicks Django so that you get to use plug and play modules,
to contribute, it's nice to know Flask well. Here are some resources which might help you:

Resources
----------

Please see the `Education <education.html>`_ section to see what you need to learn before contributing.

.. _setup:

Setup Instructions
-------------------

If you want to contribute, go ahead, we ❤️ it. We follow a 💯 % first-timers-friendly policy.

#. Make sure ``git`` is installed on your computer and ``python version 3.6`` or higher is installed. You can run the following command to check if git is installed and which python version you have. If either commands gives error then it means you need to install that software

   .. code-block:: bash

      git --version
      python --version

#. Fork repo. To do so go to the `shopyo repo <https://github.com/Abdur-rahmaanJ/shopyo>`_ and press the fork button
#. Clone the repo by running:

   .. code-block:: bash

      git clone https://github.com/<replace with your github username>/shopyo.git. 

   .. note::
    
       You can also get the clone link by clicking the green ``code`` button on your cloned shopyo repo page.
#. Next run:

   .. code-block:: bash
   
      cd <your/local/cloned/repo/path/here>

   .. note::
       The above command should be ``cd shopyo`` if you cloned using the git command above

#. Setup the python `virtual environment <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_ based on your Operating System

   For Windows OS you can do this by running:

   .. code-block:: bash

      py -m pip install --upgrade pip
      py -m venv env # you can replace env with another name that you like. For example, py -m venv shopyo-env

   For Linux and MacOS you can do this by running:

   .. code-block:: bash

      python3 -m pip install --user --upgrade pip
      python3 -m venv env # you can replace env with another name that you like. For example, python3 -m venv shopyo-env

   .. note::
      visit `virtual environment <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_ for more details 


#. Activate the `virtual environment <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_ as follows: 
   
   For Windows OS you can do this by running:

   .. code-block:: bash
      
      .\env\Scripts\activate

   For Linux and MacOS you can do this by running:

   .. code-block:: bash

      source env/bin/activate

   Now you should see something like:
    
   .. code-block:: bash

      (env) </my/path/to/shopyo> 

    
   .. note::
      ``env`` is the name of virtual environment that you setup in step 5 above.
      Make sure to always activate this ``env`` when working on ``shopyo``. If you are using
      `VS Code <https://code.visualstudio.com/>`__  then you can also add the ``"python.pythonPath"`` by creating a ``.vscode`` 
      folder at the root level and adding ``setting.json`` file to it with the content below.
      You need to replace the path with your own path to the virtual environment's ``python.exe`` 
      file and the example below is for a path in Windows OS hence the double backward slash.
      Now you can create a new terminal with virtual environment activated in VS Code using ``Ctrl`` + ``Shift`` + ````` (*control
      plus shift plus backtick character*).
      In addition, if you want to deactivate the virtual environment, run ``deactivate`` in command line

      .. code-block:: json

         {
            "python.pythonPath": "c:\\path\\to\\shopyo\\env\\Scripts\\python.exe"
         }

#. Run:

   .. code-block:: bash

      python -m pip install -U pip
      python -m pip install -r requirements.txt -r dev_requirements.txt
    
   .. note::
      This should start installing the packages required for shopyo app and might take a few seconds. If you get an error for unable to find ``requirements.txt`` make sure you are in the cloned ``shopyo`` directory and try again 

Setup Mail Dev Environment (Optional)
-------------------------------------

If you have Node.js, use the `maildev <https://github.com/maildev/maildev>`_ package. Install it using 


   .. code-block:: bash

      npm install -g maildev


Then serve it using


   .. code-block:: bash

      maildev


Dev configs for this setup:

   .. code-block:: python

      class DevelopmentConfig(Config):
          """Configurations for development"""

          ENV = "development"
          DEBUG = True
          LOGIN_DISABLED = False
          # control email confirmation for user registration
          EMAIL_CONFIRMATION_DISABLED = False
          # flask-mailman configs
          MAIL_SERVER = 'localhost'
          MAIL_PORT = 1025
          MAIL_USE_TLS = False
          MAIL_USE_SSL = False
          MAIL_USERNAME = '' # os.environ.get("MAIL_USERNAME")
          MAIL_PASSWORD = '' # os.environ.get("MAIL_PASSWORD")
          MAIL_DEFAULT_SENDER = 'ma@mail.com' # os.environ.get("MAIL_DEFAULT_SENDER")

Go to http://127.0.0.1:1080 where it serves it's web interface by default. See mails arrive in your inbox!

Syncing and continuing
----------------------


#. Next we need to setup an upstream which will allow you to update your local shopyo repo to match the owner's shopyo repo in case of any changes. You only need to do this once. To setup an upstream you do:
    
   .. code-block:: bash

      cd <your/local/cloned/repo/path/here> # not needed if you are already inside your cloned shopyo directory
      git remote add upstream https://github.com/Abdur-rahmaanJ/shopyo.git

#. Once upstream is setup, you can fetch the latest changes made to shopyo repo. Make sure to do this every time before you make branch to work on a feature. Run:
   
   .. code-block:: bash

      git fetch upstream
      git pull upstream dev

#. Do another:

   .. code-block:: bash

      cd shopyo 
      # so now your path should be something likes <your path>/shopyo/shopyo

#. Now initialize the app by running:

   .. code-block:: bash

      python manage.py initialise

#. To start the app, run: 

   .. code-block:: bash

      python manage.py runserver

#. The app should now be running on IP ``127.0.0.1`` at port# ``5000``. You can go to http://localhost:5000/ or http://127.0.0.1:5000/. You can click the login nav link or go directly to http://localhost:5000/login/. Login with email ``admin@domain.com`` and password ``pass``


Making a Pull Request
---------------------
Make sure you have setup the repo as explained in :ref:`setup` before making Pull Request (PR)

#. Let say you are excited about a feature you want to work on. You need to first create a separate branch and work on that branch. To check which branch you are currently on run ``git branch``. Most likely you will see ``dev`` branch colored green or marked to tell you that you are on ``dev`` branch. Before creating a new branch from ``dev`` make sure you have fetched latest changes as mentioned in :ref:`setup` step 9
#. To create a branch and switch to that branch you run:
   
   .. code-block:: bash

      git checkout -b <name of branch> 
      # example: git checkout -b add-form-validation

   .. note::
       You can do the above using 2 separate commands if that makes it easier:

       .. code-block:: bash
          
          # First create a new branch from current branch
          git branch <name of branch> 
          
          # Next switch to this new branch
          git checkout <name of branch to switch to> 

#. After git checkout command above, run ``git branch`` to make sure you are not working on ``dev`` branch but are on the newly created branch.
#. Now you can start working on the feature for which you want to make PR
#. Add tests for any new features that you add.
#. Run the following to make sure all the existing and new tests pass. Check the `Testing <testing.html>`_ section for more details
   
   .. code-block:: bash

      python -m pytest .

#. [*Optional Step*] Make sure to bump the version number in file ``shopyo/__init__.py`` as follows:
    * small fixes: ``_._.x``, (example ``3.4.6`` to ``3.4.7``)
    * feature, many fixes etc: ``_.x.0``, (example ``3.4.6`` to ``3.5.0``)
    * big feature, breaking change etc ``x.0.0`` (example ``3.4.6`` to ``4.0.0``)

#. Check that there are no linting errors according to ``flake8``. To do so you can run

   .. code-block:: bash

      flake8 <path of file that you want to check>
      
      # example to check the linting error for test_dashboard.py file 
      # assuming you are in shopyo/shopyo directory, run
      flake8 ./modules/box__default/dashboard/tests/test_dashboard.py

   .. note::
      If the command above returns without any output, then there are no 
      linting errors, otherwise it will tell you the line number and type
      of linting error.
      If typing ``flake8`` gives error related to command not found, then you
      do not have ``flake8`` installed and it can be installed as follows:

      .. code-block:: bash
         
         python -m pip install flake8

      In addition, if you are using `VS Code <https://code.visualstudio.com/>`__ 
      then you can create a ``.vscode`` folder at the root level and add ``setting.json`` 
      file to it with the following content. This way it auto detects the
      linting errors for you

      .. code-block:: json

         {
            "python.linting.flake8Enabled": true
         }

      If you have already created the ``setting.json`` file as mentioned in :ref:`setup` step 6,
      then your json file will look similar to one below
      
      .. code-block:: json

         {
            "python.pythonPath": "c:\\Users\\user\\Documents\\venvs\\my-shopyo-env\\Scripts\\python.exe",
            "python.linting.flake8Enabled": true
         }

#. Once you are happy with the changes you made you can double check the changed files by running:

   .. code-block:: bash

      git status

#. Next add the changes as required

   .. code-block:: bash

       git add . # to add all changes 
       git add <file1 name> <file2 name> # to only add desired files
    
#. Commit the changes. For the commit messages, follow the guidelines `here <https://udacity.github.io/git-styleguide/>`__
   
   .. code-block:: bash

      git commit -m "<put your commit message here>"

#. Finally push the committed changes from local repository to a remote repository (the one you forked)
   
   .. code-block:: bash
     
      git push origin <the current branch name>    

#. You can now make a PR. When you go to your forked repo or the owner's repo you will see a ``compare & pull request`` button. Click on it and mention the changes you made. Look at the `past PRs <https://github.com/Abdur-rahmaanJ/shopyo/pulls?q=is%3Apr+is%3Aclosed>`_ for examples of what to mention when submitting a PR. If a PR closes an issue, add ``Fixes #<issue number>``, as seen `here <https://github.com/Abdur-rahmaanJ/shopyo/pull/95>`_
#. [*Optional Step*] If you want you can request reviews when submitting PR.
#. [*Optional Step*] Add your country flag in readme after accepted PR.

.. note::
   At times when you do git status after fetching the latest changes it might say something like: ``Your branch is ahead of 'origin/dev`` which mean that your forked branch does not have the latest local changes and does not match the owner's repo. To push the latest changes to your forked repo, run:

   .. code-block:: bash

      git push origin head

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
Join the Discord community `Discord Group <https://discord.com/invite/k37Ef6w>`_

