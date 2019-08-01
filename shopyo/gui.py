from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
# create a PySide/PyQt application
app = QApplication([])
# create a PySide.QtWebKit.QWebView() to display a web page
# (your computer needs to be connected to the internet)
view = QWebView()
# setGeometry(x_pos, y_pos, width, height)
view.setGeometry(100, 150, 1200, 600)
# pick a known url
#url = "http://www.google.com/"
url = "http://localhost:5000/manufac/"
view.setWindowTitle(url)
view.load(QUrl(url))
view.show()
# run the application event loop
app.exec_()