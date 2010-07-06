

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)
web = QWebView()
web.load(QUrl("http://www.az2000.de"))
web.show()

sys.exit(app.exec_())
