#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.Qt import QRect
from PyQt4.QtGui import QWidget, QPainter, QApplication

class SecondaryWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        pDesktop = QApplication.desktop ();
        RectScreen0 = pDesktop.screenGeometry (1);
        # Se conecta a proyectores -> importa la relación de sus resoluciones.
        self.setGeometry(QRect(RectScreen0.left(), RectScreen0.top(), RectScreen0.width(), RectScreen0.height())) # x, y, w, h

    #TODO
    # Que se desplieguen las imagenes
    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 500, 500)
        dc.drawLine(500, 0, 0, 500)

class Application(QtGui.QWidget):
    
    def __init__(self):
        super(Application, self).__init__()
        
        self.initUI(800, 600)
        
    def initUI(self, w, h):               
        
        self.resize(w, h)
        self.center()
        
        self.openSTLButton = QtGui.QPushButton('Open STL')
        self.openSTLButton.clicked.connect(self.showOpenFile)
        
        self.createAnimationButton = QtGui.QPushButton('Create Animation')
        self.createAnimationButton.setEnabled(True) # TODO
        self.createAnimationButton.clicked.connect(self.createImage)

        # Messages
        path_message = ""
        open_stl_message = "<h3>Please, select the STL file you want to print</h3>"
        creating_message = "<h3>When you are ready press Print to start printing</h3>"

        self.pathLabel = QtGui.QLabel(path_message)
        self.openLabel = QtGui.QLabel(open_stl_message)
        self.printLabel = QtGui.QLabel(creating_message)

        # Layout
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.openLabel, 1, 0)
        grid.addWidget(self.openSTLButton, 1, 2)

        #grid.addWidget(self.pathLabel, 2, 0)
        
        grid.addWidget(self.printLabel, 2, 0)
        grid.addWidget(self.createAnimationButton, 2, 2)

        self.setLayout(grid)
        self.setWindowTitle('DLI3D')    
        self.show()
        
    def showOpenFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home', self.tr("STL Files (*.stl)"))
        if fileName:
            openFile = open(fileName, 'r')
            ##createImages(openFile)
            self.createAnimationButton.setEnabled(True)
            self.pathLabel.setText('<h3>'+ fileName +'</h3>')                      

    def createImage(self):
        self.w = SecondaryWindow()
        self.w.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
