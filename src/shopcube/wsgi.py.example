# +++++++++++ FLASK +++++++++++
# Flask works like any other WSGI-compatible framework, we just need
# to import the application.  Often Flask apps are called "app" so we
# may need to rename it during the import:
#
#
import os
import sys

sys.path.append(os.getcwd())
from app import create_app

#
# The "/home/appinv" below specifies your home
# directory -- the rest should be the directory you uploaded your Flask
# code to underneath the home directory.  So if you just ran
# "git clone git@github.com/myusername/myproject.git"
# ...or uploaded files to the directory "myproject", then you should
# specify "/home/appinv/myproject"
# on shell do pwd to get a path like this:'/home2/folder/shopyo/shopyo' set path to this
path = ""
if path not in sys.path:
    sys.path.insert(0, path)
#


application = create_app("production")

#
# NB -- many Flask guides suggest you use a file called run.py; that's
# not necessary on PythonAnywhere.  And you should make sure your code
# does *not* invoke the flask development server with app.run(), as it
# will prevent your wsgi file from working.
# whatever app you specify, modify that
