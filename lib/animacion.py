import os
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QRect
from PyQt4.QtGui import QWidget, QPainter, QApplication
import PIL
from PIL import Image

def is_image(filename):
    """ File is image if it has a common suffix and it is a regular file """

    if not os.path.isfile(filename):
        return False

    for suffix in ['.jpg', '.png', '.bmp']:
        if filename.lower().endswith(suffix):
            return True

    return False

def load_file_list(folder):
    """ Find all images """
    if folder[:-1]!="/":
        folder = folder + "/"
    files = []
    images = []
    index = 0
    for filename in os.listdir(folder):
        files.append(folder+filename)
        #print filename
    return files

class Display_images(QWidget):#QWidget):
 
    
    __pyqtSignals__ = ("timeChanged(QTime)", "timeZoneChanged(int)")
    
    def __init__(self, folder ='./animacion/', parent = None, seconds = 1, arduino):
    
        #QtGui.QWidget.__init__(self, parent)
        #QtGui.QDialog.__init__(self, parent)
        QWidget.__init__(self)
        pDesktop = QApplication.desktop ()

        self.folder = folder
        self.time_to_change = int(seconds*1000)
        self.black_time = 1000 
        
        self.arduino = arduino
        print "t = ",self.time_to_change, " tb = ", self.black_time
        self.timeZoneOffset = 0

        self.i = 0
        self.num_imagen = 0
        self.para_blanco = 0
        self.time = QtCore.QTime.currentTime()
        
        timer = QtCore.QTimer(self)
        self.connect(timer, QtCore.SIGNAL("timeout()"), self, QtCore.SLOT("update()"))
        self.connect(timer, QtCore.SIGNAL("timeout()"), self.updateTime)
        timer.start(1)

        self.imagenes = load_file_list(self.folder)
        
        self.label =  QtGui.QLabel(self)
        self.label.setStyleSheet("QLabel { background-color : black;}");
        self.label.setScaledContents(True)
        
        self.setWindowTitle(QtCore.QObject.tr(self, "DLI3D"))
        self.resize(800, 600)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.label, 1,0)

        self.setLayout(grid)

        RectScreen0 = pDesktop.screenGeometry (1);
        # Se conecta a proyectores -> importa la relacion de sus resoluciones.
        self.setGeometry(QRect(RectScreen0.left(), RectScreen0.top(), RectScreen0.width(), RectScreen0.height())) # x, y, w, h
        self.show()

    def paintEvent(self, event):

        time = QtCore.QTime.currentTime()

        ahora = time.hour()*60*60*1000+time.minute()*60*1000+time.second()*1000+time.msec()

        anterior = self.time.hour()*60*60*1000+self.time.minute()*60*1000+self.time.second()*1000+self.time.msec()

        
        #time = time.addSecs(self.timeZoneOffset * 3600)
        #time = time.addMSecs(self.timeZoneOffset * 3600000)
        #now = time.second()

        #print "ahora = ", ahora, "anterior = ", anterior

        if self.para_blanco%2 == 1:
            #print "para blanco: ", self.para_blanco
            if (anterior + self.black_time < ahora ) and (self.num_imagen < len(self.imagenes)):
                #print "cambia: ", self.imagenes[self.num_imagen]                
                self.label.setPixmap(QtGui.QPixmap(self.imagenes[self.num_imagen]))
                self.num_imagen += 1
                self.para_blanco += 1
                self.time = time
        else:
            #print "para blanco: ", self.para_blanco
            if (anterior + self.time_to_change  < ahora ):   
                #print "borrar"
                self.label.clear()
                arduino.move_up()
                self.para_blanco += 1
                self.time = time

        if self.num_imagen >= len(self.imagenes):
            self.label.clear()

    
    def minimumSizeHint(self):
    
        return QtCore.QSize(50, 50)
    
    def sizeHint(self):
    
        return QtCore.QSize(100, 100)
    
    def updateTime(self):
    
        self.emit(QtCore.SIGNAL("timeChanged(QTime)"), QtCore.QTime.currentTime())
    
    # The timeZone property is implemented using the getTimeZone() getter
    # method, the setTimeZone() setter method, and the resetTimeZone() method.
    
    # The getter just returns the internal time zone value.
    def getTimeZone(self):
    
        return self.timeZoneOffset
    
    # The setTimeZone() method is also defined to be a slot. The @pyqtSignature
    # decorator is used to tell PyQt which argument type the method expects,
    # and is especially useful when you want to define slots with the same
    # name that accept different argument types.
    
    @QtCore.pyqtSignature("setTimeZone(int)")
    def setTimeZone(self, value):
    
        self.timeZoneOffset = value
        self.emit(QtCore.SIGNAL("timeZoneChanged(int)"), value)
        self.update()
    
    # Qt's property system supports properties that can be reset to their
    # original values. This method enables the timeZone property to be reset.
    def resetTimeZone(self):
    
        self.timeZoneOffset = 0
        self.emit(QtCore.SIGNAL("timeZoneChanged(int)"), 0)
        self.update()
    
    # Qt-style properties are defined differently to Python's properties.
    # To declare a property, we call pyqtProperty() to specify the type and,
    # in this case, getter, setter and resetter methods.
    timeZone = QtCore.pyqtProperty("int", getTimeZone, setTimeZone, resetTimeZone)


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    clock = Display_images()
    
    sys.exit(app.exec_())
