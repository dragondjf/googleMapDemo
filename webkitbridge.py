#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from PySide import QtWebKit
from PySide import QtNetwork


class WebkitBasePage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WebkitBasePage, self).__init__(parent)
        self.parent = parent
        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        QtWebKit.QWebSettings.globalSettings().setAttribute(
            QtWebKit.QWebSettings.PluginsEnabled, True)

        self.view = QtWebKit.QWebView(self)
        self.view.setFocus()

        self.setupInspector()
        self.splitter = QtGui.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Vertical)

        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.webInspector)

        mainlayout = QtGui.QVBoxLayout(self)
        mainlayout.addWidget(self.splitter)
        self.setLayout(mainlayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def setupInspector(self):
        page = self.view.page()
        page.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QtWebKit.QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QtGui.QShortcut(self)
        shortcut.setKey('F12')
        shortcut.activated.connect(self.toggleInspector)
        self.webInspector.setVisible(False)

    def toggleInspector(self):
        self.webInspector.setVisible(not self.webInspector.isVisible())


class DBrowser(WebkitBasePage):

    sin = QtCore.Signal('int')

    def __init__(self, parent=None):
        super(DBrowser, self).__init__(parent)
        self.width = QtGui.QApplication.desktop().availableGeometry().width() * 0.8
        self.height = QtGui.QApplication.desktop().availableGeometry().height() * 0.8
        self.setFixedSize(self.width, self.height)

        self.view.page().mainFrame().javaScriptWindowObjectCleared.connect(self.populateJavaScriptWindowObject)
        self.view.loadFinished.connect(self.finishLoading)
        self.view.load(QtCore.QUrl("test.html"))

    def finishLoading(self):
        print 'loadFinished'
        # self.sin.emit()

    @QtCore.Slot()
    def slotThatEmitsSignal(self):
        self.sin.emit(3)

    def populateJavaScriptWindowObject(self):
        self.view.page().mainFrame().addToJavaScriptWindowObject('DBrowser', self)

    @QtCore.Slot()
    def calledByJs(self):
        print 'this function called by js'

    @QtCore.Slot(str)
    def calledByJs_str(self, message):
        print 'this function called by js with [str]'
        print message

    @QtCore.Slot(int)
    def calledByJs_int(self, num):
        print 'this function called by js with [int]'
        print num

    @QtCore.Slot('QList')
    def calledByJs_object(self, l):
        print 'this function called by js with [list]'
        print l


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    browser = DBrowser()
    browser.show()
    app.exec_()

if __name__ == '__main__':
    main()
