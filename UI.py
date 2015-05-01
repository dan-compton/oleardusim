# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GCS.ui'
#
# Created: Wed Nov  2 13:40:51 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from GCS import GCS
import XPlane
import ArduPilot
from FlightPathScheduling import AStar

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def initGCS(self):
        self.GCS = GCS()
        x1 = XPlane.XPlane('131.204.27.9', 49005, '131.204.27.8', 49000,self.GCS,0)
        a1 = ArduPilot.ArduPilot('/dev/ttyUSB0',38400,self.GCS,0)
        self.GCS.addPair(a1,x1)
        x1.execute()
        a1.execute()

    def writeNextWaypoint(self):
        # Write the GPS Waypoint
        lat = float(self.latTextBox.text())
        lng = float(self.lngTextBox.text())
        alt = float(self.altTextBox.text())
        goal = (lat,lng,alt,)
        self.GCS.ID_to_ardu[0].setGoal(goal)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mapWebKit = QtWebKit.QWebView(self.centralwidget)
        self.mapWebKit.setGeometry(QtCore.QRect(389, 0, 411, 561))
        self.mapWebKit.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.mapWebKit.setObjectName(_fromUtf8("mapWebKit"))
        self.writeNextWaypointButton = QtGui.QPushButton(self.centralwidget)
        self.writeNextWaypointButton.setGeometry(QtCore.QRect(219, 520, 151, 26))
        self.writeNextWaypointButton.setText(QtGui.QApplication.translate("MainWindow", "write next waypoint", None, QtGui.QApplication.UnicodeUTF8))
        self.writeNextWaypointButton.setObjectName(_fromUtf8("writeNextWaypointButton"))
        QtCore.QObject.connect(self.writeNextWaypointButton, QtCore.SIGNAL("clicked()"),self.writeNextWaypoint)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(370, 0, 20, 551))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.latTextBox = QtGui.QLineEdit(self.centralwidget)
        self.latTextBox.setGeometry(QtCore.QRect(260, 430, 113, 25))
        self.latTextBox.setObjectName(_fromUtf8("latTextBox"))
        self.lngTextBox = QtGui.QLineEdit(self.centralwidget)
        self.lngTextBox.setGeometry(QtCore.QRect(260, 460, 113, 25))
        self.lngTextBox.setObjectName(_fromUtf8("lngTextBox"))
        self.altTextBox = QtGui.QLineEdit(self.centralwidget)
        self.altTextBox.setGeometry(QtCore.QRect(260, 490, 113, 25))
        self.altTextBox.setObjectName(_fromUtf8("altTextBox"))
        self.latLabel = QtGui.QLabel(self.centralwidget)
        self.latLabel.setGeometry(QtCore.QRect(200, 440, 57, 15))
        self.latLabel.setText(QtGui.QApplication.translate("MainWindow", "lat:", None, QtGui.QApplication.UnicodeUTF8))
        self.latLabel.setObjectName(_fromUtf8("latLabel"))
        self.lngLabel = QtGui.QLabel(self.centralwidget)
        self.lngLabel.setGeometry(QtCore.QRect(200, 460, 57, 15))
        self.lngLabel.setText(QtGui.QApplication.translate("MainWindow", "lng:", None, QtGui.QApplication.UnicodeUTF8))
        self.lngLabel.setObjectName(_fromUtf8("lngLabel"))
        self.altLabel = QtGui.QLabel(self.centralwidget)
        self.altLabel.setGeometry(QtCore.QRect(200, 490, 57, 15))
        self.altLabel.setText(QtGui.QApplication.translate("MainWindow", "alt:", None, QtGui.QApplication.UnicodeUTF8))
        self.altLabel.setObjectName(_fromUtf8("altLabel"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.initGCS()
    MainWindow.show()
    sys.exit(app.exec_())
