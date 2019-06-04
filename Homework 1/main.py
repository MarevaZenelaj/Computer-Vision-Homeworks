import sys
from PIL import Image
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMenuBar, QDesktopWidget, QFileDialog,QGridLayout, QVBoxLayout,QGroupBox, QFrame, QLabel, QHBoxLayout, QSplitter, qApp, QApplication, QWidget, QPushButton,QAction, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from histogram_match_calculate_f import *

class HistEqualizer(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Histogram Equalization'
        
        groupBox = QGroupBox('Input')
        label1 = QLabel(groupBox)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        groupBox2 = QGroupBox('Target')
        vbox2 = QVBoxLayout()
        vbox2.addStretch(1)
        groupBox2.setLayout(vbox2)

        groupBox3 = QGroupBox('Result')
        vbox3 = QVBoxLayout()
        vbox3.addStretch(1)
        groupBox3.setLayout(vbox3)
        
        grid = QGridLayout()
        grid.setSpacing(50)
        grid.addWidget(groupBox, 0,0,0,-1)
        grid.addWidget(groupBox2,0,1,0,-1)
        grid.addWidget(groupBox3, 0,2,0,-1)
        self.setLayout(grid)
        self.initUI()
        
    def open_image(self):
        
        path_file = self.OpenFileNameDialog()
        path = path_file[0]
        img = cv2.imread(path)
        label = QLabel(self)
        pixmap = QPixmap(path)
        print(pixmax.isNull())
        label.setPixmap(pixmap)
        label.show()
        return img
    
    def equal_hist(img1, img2):
        new_img = equalize_histogram(img, img1)
        new_image = Image.fromarray(new_img)
        new_image.show()
        name = 'equalizedImage.png'
        new_img.save(name)
        
        
    def OpenFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName
        
    def initUI(self):
        
        exitAct = QAction(QIcon('exit.png'),'&Exit', self)
        exitAct.triggered.connect(qApp.quit) 
        openInput = QAction('&Open Input', self)
        img1 = openInput.triggered.connect(self.open_image)
        openTarget = QAction('&Open Target', self)
        img2 = openTarget.triggered.connect(self.open_image)
        
        menubar = QMenuBar(self)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openInput)
        fileMenu.addAction(openTarget)
        fileMenu.addAction(exitAct)
        
        self.setWindowTitle(self.title)
        self.setContentsMargins(0,35,0,0)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        button = QPushButton('Equalize Histogram', self)
        button.move(0,20)
        screenShape = QDesktopWidget().screenGeometry()
        width = screenShape.width()
        button.resize(width,25)
        button.setStyleSheet("Text-align:left");
        button.clicked.connect(self.equal_hist)   
        self.show()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HistEqualizer()
    sys.exit(app.exec_())
