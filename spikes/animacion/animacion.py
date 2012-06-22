import os
from PyQt4 import QtCore, QtGui
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
    files = []
    images = []
    index = 0
    for filename in os.listdir(folder):
        files.append(folder+filename)
    return files

class Display_images(QtGui.QWidget):
 
    
    __pyqtSignals__ = ("timeChanged(QTime)", "timeZoneChanged(int)")
    
    def __init__(self, folder ='./imagenes/'):
    
        QtGui.QWidget.__init__(self, None)

        self.folder = folder
        self.timeZoneOffset = 0

        self.i = 0
        self.para_blanco = 0
        self.time = QtCore.QTime.currentTime()
        
        timer = QtCore.QTimer(self)
        self.connect(timer, QtCore.SIGNAL("timeout()"), self, QtCore.SLOT("update()"))
        self.connect(timer, QtCore.SIGNAL("timeout()"), self.updateTime)
        timer.start(1)

        self.imagenes = load_file_list(folder)
        
        self.label =  QtGui.QLabel(self)
        self.label.setPixmap(QtGui.QPixmap("white.jpg"))
        self.label.setScaledContents(True)
        
        self.setWindowTitle(QtCore.QObject.tr(self, "DLI3D"))
        self.resize(600, 600)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.label, 1,0)

        self.setLayout(grid)

        self.show()

    def paintEvent(self, event):

        time = QtCore.QTime.currentTime()

        ahora = time.hour()*60*60*1000+time.minute()*60*1000+time.second()*1000+time.msec()

        anterior = self.time.hour()*60*60*1000+self.time.minute()*60*1000+self.time.second()*1000+self.time.msec()

        
        #time = time.addSecs(self.timeZoneOffset * 3600)
        #time = time.addMSecs(self.timeZoneOffset * 3600000)
        #now = time.second()

        if anterior + 1000 < ahora and self.i < len(self.imagenes):

            self.para_blanco += 1

            if self.para_blanco%2 == 1:
                self.label.setPixmap(QtGui.QPixmap("white.jpg"))
            else:
                self.i += 1
                archivo = self.imagenes[self.i]
                self.label.setPixmap(QtGui.QPixmap(archivo))

            print self.time
            print time
            print "----"

                       

            self.time = time
            


        #painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))

        #painter.rotate(6.0 * (time.minute() + time.second() / 60.0))

    
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