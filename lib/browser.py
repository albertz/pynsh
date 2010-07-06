

import sys, webbrowser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)
web = QWebView()

web.setHtml(file("html/main.html").read())
web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)


def linkClicked(url): webbrowser.open(str(url.toString()))
web.connect(web, SIGNAL("linkClicked (const QUrl&)"), linkClicked) 

web.show()

# testcode
if False:
	try:
		from IPython.Shell import IPShellEmbed
		ipshell = IPShellEmbed(argv=[''],banner="hello!",exit_msg="Goodbye")
		ipshell()
	except ImportError:
		import code
		# calling this with globals ensures we can see the environment
		shell = code.InteractiveConsole(globals())
		shell.interact()

web.page().mainFrame().evaluateJavaScript("addHtml('<a href=http://www.az2000.de>www.az2000.de</a>')")

sys.exit(app.exec_())
