#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from slices import createSlices

class Application(QtGui.QWidget):
    
    def __init__(self):
        super(Application, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        self.resize(800, 600)
        self.center()
        
        self.heightInput = QtGui.QLineEdit()
        self.outputInput = QtGui.QLineEdit()
        self.stepInput = QtGui.QLineEdit()
        self.layerInput = QtGui.QLineEdit()
        
        self.openSTLButton = QtGui.QPushButton('Open STL')
        self.openSTLButton.clicked.connect(self.showOpenFile)
        
        self.createAnimationButton = QtGui.QPushButton('Print')
        self.createAnimationButton.setEnabled(False)
##        createAnimationButton.clicked.connect(self.makeAnimation)

        welcome = QtGui.QLabel('<h1>Welcome</h1>', self)
        self.printLabel = QtGui.QLabel('<h3>When you are ready press Print to start printing</h3>')
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(QtGui.QLabel('<h2>Height</h2>'), 0 , 0)
        grid.addWidget(self.heightInput, 0, 1)
        grid.addWidget(QtGui.QLabel('<h2>Output Directory</h2>'), 1 , 0)
        grid.addWidget(self.outputInput, 1, 1)
        grid.addWidget(QtGui.QLabel('<h2>Step</h2>'), 1 , 0)
        grid.addWidget(self.stepInput, 1, 1)
        grid.addWidget(QtGui.QLabel('<h2>Layer Thickness</h2>'), 1 , 0)
        grid.addWidget(self.layerInput, 1, 1)
        
        grid.addWidget(QtGui.QLabel('<h3>Please, select the STL file you want to print</h3>'), 1,0)
        grid.addWidget(self.printLabel, 2,0)
        grid.addWidget(self.openSTLButton, 1, 2)
        grid.addWidget(self.createAnimationButton, 2, 2)
        
        self.setLayout(grid)
        self.setWindowTitle('DLI3D')    
        self.show()
        
    def showOpenFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home', self.tr("STL Files (*.stl)"))
        if fileName:
            createImages(fileName)
            self.createAnimationButton.setEnabled(True)
            self.printLabel.setText('<h3>When you are ready press Print to start printing '  + fileName + '</h3>')                                        
    def createImages(self, fileName):
        createSlices(self.heightInput.text, self.outputInput.text, fileName, self.stepInput.text, self.layerInput.text)
    
##    def makeAnimation(self):
        ##insertar el codigo que crea la animación
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
