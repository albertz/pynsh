

import sys, webbrowser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)
web = QWebView()
web.setHtml(file("html/main.html").read())

web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
web.linkClicked.connect(lambda url: webbrowser.open(str(url.toString())))

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

	testProp = pyqtProperty(str, fget = lambda _: sys.version)
		
web.page().mainFrame().addToJavaScriptWindowObject("Pynsh", PynshJS())

def jsEscape(s): return s.replace("\"", "&quot;")
def jsString(s): return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\""

def simpleJsLink(jscode, title="do it"):
	return jsString("<a href=\"javascript:" + jsEscape(jscode) + "\">" + title + "</a>")

jsCall = web.page().mainFrame().evaluateJavaScript

jsCall("addHtml(" + simpleJsLink("alert(\"Hello from JS\")", "hello") + ")")
jsCall("addHtml(" + simpleJsLink("Pynsh.testFunc(Pynsh.testProp)", "test") + ")")


sys.exit(app.exec_())
