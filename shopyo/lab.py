# see https://pythonhosted.org/PyDrive/quickstart.html
# see https://pythonhosted.org/PyDrive/oauth.html#sample-settings-yaml
# see https://github.com/googledrive/PyDrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import webbrowser
import datetime
# Create local webserver and auto handles authentication.
# Standard webbrowser gave an error, JonB found the solution
if not hasattr(webbrowser, '_open'):
    webbrowser._open = webbrowser.open


def wbopen(url, *args, **kwargs):
    return webbrowser._open(url)


webbrowser.open = wbopen

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

# upload
drive = GoogleDrive(gauth)


# Create GoogleDriveFile instance.
file1 = drive.CreateFile(
    {'title': 'shopyo__db_{}.db'.format(
        datetime.datetime.now().strftime("%d_%m_%Y__%H_%M_%S"))})
file1.SetContentFile('test.db')  # Set content of the file from given string.
file1.Upload()
