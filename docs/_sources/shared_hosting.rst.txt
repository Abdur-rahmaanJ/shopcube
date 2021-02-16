.. :tocdepth:: 5

Deploy to shared hosting
========================

Describes the process to deploy to shared hosting like namecheap


All steps
----------

Go to CPanel

Choose Terminal

Navigate to the folder you will clone shopyo (typically at domain.com folder or subdomain.domain.com folder).
See File manager for that

Clone shopyo

.. code-block:: bash

    git clone https://github.com/Abdur-rahmaanJ/shopyo.git


Now on control panel open setup python app

Set the following values

* Python version: 3.7 works well

* Application root: folder/shopyo/shopyo

* Application URL: choose subdomain or adjust ad needed

* Application startup file: wsgi.py

* Application Entry point: application

Now it will override your wsgi.py, edit the file and add the initial info on github

Set path = '' in wsgi.py to what you get when on terminal you navigate to folder/shopyo/shopyo and type pwd
It needs the absolute file

You also get the path when editing wsgi.py, add everything except /wsgi.py

Now initialise app. On the python app page it will give you an instruction to copy to activate virtual env

paste in terminal and press enter

.. code-block:: bash

    python3 -m pip install requirements.txt

    export FLASK_APP=app.py

    python3 manage.py initialise


go to setup python app then restart app

go to your url

go to url/dashboard for login



