#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt4 import QtGui
sys.path.append(os.path.join(os.getcwd(), '..', 'lib'))

from slices import *

class Application(QtGui.QWidget):
    
    def __init__(self):
        super(Application, self).__init__()
        
        self.initUI()
    def checker(self):
        if self.heightInput.text()!='' and self.stepInput.text()!='' and self.layerInput.text()!='':
            self.openSTLButton.setEnabled(True)
        else:
            self.openSTLButton.setEnabled(False)
    
    def initUI(self):
        
        self.resize(800, 600)
        self.center()
        
        self.heightInput = QtGui.QLineEdit()
        self.stepInput = QtGui.QLineEdit()
        self.layerInput = QtGui.QLineEdit()
        
#        self.layerInput.textChanged('',self.checker())
#        self.layerInput.textChanged('',self.checker())
#        self.layerInput.textChanged(self.checker())
        

        
        self.dirLabel = QtGui.QLabel('Output Directory')
        self.stlLabel = QtGui.QLabel('Please, select the STL file you want to print')
        
        self.outputFileName = ''
        self.outputButton = QtGui.QPushButton('Open Folder')
        self.outputButton.clicked.connect(self.showOpenFileOutput)
         
        self.openSTLButton = QtGui.QPushButton('Open STL')
        self.openSTLButton.clicked.connect(self.showOpenFile)
        self.openSTLButton.setEnabled(False)
        
        self.createAnimationButton = QtGui.QPushButton('Print')
        self.createAnimationButton.setEnabled(False)
## createAnimationButton.clicked.connect(self.makeAnimation)

        #welcome = QtGui.QLabel('<h1>Welcome</h1>', self)
        self.printLabel = QtGui.QLabel('When you are ready press Print to start printing')
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(QtGui.QLabel('Height'), 0 , 0)
        grid.addWidget(self.heightInput, 0, 2)
        grid.addWidget(QtGui.QLabel('Step'), 1 , 0)
        grid.addWidget(self.stepInput, 1, 2)
        grid.addWidget(QtGui.QLabel('Layer Thickness'), 2 , 0)
        grid.addWidget(self.layerInput, 2, 2)
        grid.addWidget(self.dirLabel, 3 , 0)
        grid.addWidget(self.outputButton, 3, 2)
        
        grid.addWidget(self.stlLabel, 4,0)
        grid.addWidget(self.printLabel, 5,0)
        grid.addWidget(QtGui.QLabel(''), 4 , 1)
        grid.addWidget(self.openSTLButton, 4, 2)
        grid.addWidget(self.createAnimationButton, 5, 2)
        
        self.setLayout(grid)
        self.setWindowTitle('DLI3D')
        self.show()
        
    def createImages(self,fileName):
        createSlices(self.heightInput.text(), str(self.outputFileName)+'.jpg', str(fileName), self.stepInput.text(), self.layerInput.text())
    
    def showOpenFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                '/home', self.tr("STL Files (*.stl)"))
        if fileName:
            self.stlLabel.setText('Selected STL file'+fileName)
            self.createImages(fileName)
            self.createAnimationButton.setEnabled(True)
            self.printLabel.setText('When you are ready press Print to start printing ' + fileName)
    
    def showOpenFileOutput(self):
        dirName = QtGui.QFileDialog.getExistingDirectory(self, 'Open directory',
                '/home')
        if dirName:
         self.outputFileName = dirName
         self.dirLabel.setText("Selected directory: " + dirName)
         self.checker()
    
## def makeAnimation(self):
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