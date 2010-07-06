

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

class PynshJS(QObject):
	@pyqtSlot(str)
	def testFunc(self, msg):
		print "test from JS:", msg

	#def testProp(self):
	#	return sys.version

	testProp = pyqtProperty(str, fget = lambda _: sys.version)
		
web.page().mainFrame().addToJavaScriptWindowObject("Pynsh", PynshJS())

def jsEscape(s): return s.replace("\"", "&quot;")
def javascriptString(s): return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\""

def simpleJsLink(jscode, title="do it"):
	return javascriptString("<a href=\"javascript:" + jsEscape(jscode) + "\">" + title + "</a>")

web.page().mainFrame().evaluateJavaScript("addHtml(" + simpleJsLink("alert(\"Hello from JS\")", "hello") + ")")
web.page().mainFrame().evaluateJavaScript("addHtml(" + simpleJsLink("Pynsh.testFunc(Pynsh.testProp)", "test") + ")")

sys.exit(app.exec_())
