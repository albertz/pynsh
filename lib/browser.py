

import sys, webbrowser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)
web = QWebView()

web.load(QUrl("http://www.az2000.de/projects/javascript-project/"))
web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)


def linkClicked(url): webbrowser.open(str(url.toString()))
web.connect(web, SIGNAL("linkClicked (const QUrl&)"), linkClicked) 


web.show()

sys.exit(app.exec_())
