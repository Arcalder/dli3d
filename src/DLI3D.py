#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt4 import QtGui
from PyQt4.Qt import QRect
from PyQt4.QtGui import QWidget, QPainter, QApplication
sys.path.append(os.path.join(os.getcwd(), '..', 'lib'))

from slices import *
from animacion import *

'''
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
'''
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
        self.secondsInput = QtGui.QLineEdit()
        self.arduinoPortInput = QtGui.QLineEdit()
        
#        self.layerInput.textChanged('',self.checker())
#        self.layerInput.textChanged('',self.checker())
#        self.layerInput.textChanged(self.checker())
        

        
        self.dirLabel = QtGui.QLabel('Output Directory')
        self.stlLabel = QtGui.QLabel('Please, select the STL file you want to print')
        
        self.outputFileName = ''
        self.outputButton = QtGui.QPushButton('Select Folder')
        self.outputButton.clicked.connect(self.showOpenFileOutput)
         
        self.openSTLButton = QtGui.QPushButton('Open STL to create the slices: must be a valid STL, check "restriction.jpg"')
        self.openSTLButton.clicked.connect(self.showOpenFile)
        self.openSTLButton.setEnabled(False)
        
        self.createAnimationButton = QtGui.QPushButton('Print')
        self.createAnimationButton.setEnabled(False)
        self.createAnimationButton.clicked.connect(self.makeAnimation)

        #welcome = QtGui.QLabel('<h1>Welcome</h1>', self)
        self.printLabel = QtGui.QLabel('When you are ready press Print to start printing')
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(QtGui.QLabel('Height'), 0 , 0)
        grid.addWidget(self.heightInput, 0, 2)
        grid.addWidget(QtGui.QLabel('Step'), 1 , 0)
        grid.addWidget(self.stepInput, 1, 2)
        grid.addWidget(QtGui.QLabel('Layer Thickness (for slicing with a disk (height of disk))'), 2 , 0)
        grid.addWidget(self.layerInput, 2, 2)
        grid.addWidget(QtGui.QLabel('Seconds of exposure'), 3 , 0)
        grid.addWidget(self.secondsInput, 3, 2)
        grid.addWidget(QtGui.QLabel('Arduino Port'), 4 , 0)
        grid.addWidget(self.arduinoPortInput, 4, 2)

        grid.addWidget(self.dirLabel, 5 , 0)
        grid.addWidget(self.outputButton, 5, 2)
        
        grid.addWidget(self.stlLabel, 6,0)
        grid.addWidget(self.openSTLButton, 6, 2)

        grid.addWidget(self.printLabel, 7,0)
        grid.addWidget(QtGui.QLabel(''), 7 , 1)
        grid.addWidget(self.createAnimationButton, 7, 2)
        
        self.setLayout(grid)
        self.setWindowTitle('DLI3D')
        self.show()
        
    def createImages(self,fileName):
        exec_id = 'EXEC_ID'
        output_path = os.path.join(str(self.outputFileName), "%s.%s" % (exec_id, 'jpg'))
        createSlices(self.heightInput.text(), output_path, str(fileName), self.stepInput.text(), self.layerInput.text())
    
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
    
    def makeAnimation(self):
        ##insertar el codigo que crea la animación
        #self.secondWindow = SecondaryWindow()    
        print "forder = ", self.outputFileName  
        self.display_window = Display_images( parent = self, folder = self.outputFileName, seconds = int(self.secondsInput.text()) )
        #self.display_window.show()
        #self.secondWindow.show()
        
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
