import sys
from PIL import Image
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMenuBar, QDesktopWidget, QFileDialog,QGridLayout, QVBoxLayout,QGroupBox, QFrame, QLabel, QHBoxLayout, QSplitter, qApp, QApplication, QWidget, QPushButton,QAction, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QPolygon, QPainter, QColor, QPen
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, QPoint
from PyQt5.QtCore import Qt

from start import *

import numpy as np
import cv2

def readP(filename):
    points = []
    with open(filename) as file:
        for row in file:
            x,y = row.split()
            points.append((int(x),int(y)))
    return points

class Morph(QWidget):
 
    def __init__(self):
        super().__init__()
        self.boxes = [QGroupBox(), QGroupBox(), QGroupBox()]
        self.labels = [QLabel(),QLabel(),QLabel()]
        self.paths = []
        self.triangle_list = []
        self.title = 'Image Morphing'
        self.label_pos = [[21, 204],[476,204]]
        #self.points = []
        self.boxes[0] = QGroupBox('Input')
        label1 = QLabel(self.boxes[0])
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.labels[0])
        self.boxes[0].setLayout(vbox)

        self.boxes[1] = QGroupBox('Target')
        vbox2 = QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.labels[1])
        self.boxes[1].setLayout(vbox2)

        self.boxes[2] = QGroupBox('Result')
        vbox3 = QVBoxLayout()
        vbox3.addStretch(1)
        vbox3.addWidget(self.labels[2])
        self.boxes[2].setLayout(vbox3)
        
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.boxes[0], 0,0,0,-1)
        grid.addWidget(self.boxes[1],0,1,0,-1)
        grid.addWidget(self.boxes[2], 0,2,0,-1)
        self.setLayout(grid)
        self.initUI()

        
    def open_input(self):
        
        path_file = self.OpenFileNameDialog()
        path = path_file[0]
        self.paths.append(path)
        self.boxes[0].setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(path)
        #self.labels[0].resize(pixmap.width(), pixmap.height())
        self.labels[0].setPixmap(pixmap)
        self.labels[0].show()
        
    '''def paintEvent(self, e):
       qp = QPainter()
       qp.begin(self)
       self.drawPoints(qp)
       qp.end()

    def drawPoints(self, qp):
        if self.labels[0].pixmap():
           qp.drawPixmap(self.rect(), self.labels[0].pixmap())
           qp.setPen(Qt.red)
        
           for i in range(len(self.points)):
              qp.drawPoint(self.points[i][0], self.points[i][1]) '''      

    '''def mouseReleaseEvent(self, QMouseEvent):
        x = QMouseEvent.x()     
        y = QMouseEvent.y()
        #self.points.append([x,y])
        f=open("points_main.txt", "a+")
        f.write("%d %d\n" % (int(x),int(y)))
        f.close()

        if x < 470:
                x_ = x - self.label_pos[0][0]
                y_ = y - self.label_pos[0][1]
                f1=open("points1.txt", "a+")
                f1.write("%d %d\n" % (int(x_),int(y_)))
                f1.close()
        else:
                x_ = x - self.label_pos[1][0]
                y_ = y - self.label_pos[1][1]
                f2=open("points2.txt", "a+")
                f2.write("%d %d\n" % (int(x_),int(y_)))
                f2.close()

        #print(self.labels[0].mapToGlobal(x))
        #self.update()'''
    

    def open_target(self):
        path_file = self.OpenFileNameDialog()
        path = path_file[0]
        self.paths.append(path)
        self.boxes[1].setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(path)
        self.labels[1].setPixmap(pixmap)
        self.labels[1].show()
        
   
        
    
    def morph(self):
    
        alpha = 0.5
        img1 = cv2.imread(self.paths[0]);
        img2 = cv2.imread(self.paths[1]);
        img1 = np.float32(img1)
        img2 = np.float32(img2)

        points1 = readP('points1.txt')
        points2 = readP('points2.txt')
        points = [];

    # Compute weighted average point coordinates
        for i in range(0, len(points1)):
                x = ( 1 - alpha ) * points1[i][0] + alpha * points2[i][0]
                y = ( 1 - alpha ) * points1[i][1] + alpha * points2[i][1]
                points.append((x,y))
                

    # Allocate space for final output
        imgMorph = np.zeros(img1.shape, dtype = img1.dtype)

        for line in self.triangles:
            x,y,z = line.split()
            
            x = int(x)
            y = int(y)
            z = int(z)
            
            t1 = [points1[x], points1[y], points1[z]]
            t2 = [points2[x], points2[y], points2[z]]
            t = [ points[x], points[y], points[z] ]
            morph_images_triangle(img1, img2, imgMorph, t1, t2, t, alpha)

        cv2.imwrite("morphed.jpg",imgMorph) 
        self.show_result()


    def show_result(self):
        path = "C:\\Users\\Mareva Zenelaj\\Desktop\\ITU 7th semester\\Computer Vision\\Homeworks\\HW 3\\morphed.jpg"
        self.boxes[2].setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(path)
        self.labels[2].setPixmap(pixmap)
        self.labels[2].show()
        

    def triangulation(self):
        self.triangle_list = triangulation_delaunay('Arnie.jpg')


    def OpenFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName
        

    def initUI(self):
        
        exitAct = QAction(QIcon('exit.png'),'&Exit', self)
        exitAct.triggered.connect(qApp.quit) 
        openInput = QAction('&Open Input', self)
        img1 = openInput.triggered.connect(self.open_input)
        openTarget = QAction('&Open Target', self)
        img2 = openTarget.triggered.connect(self.open_target)
        
        menubar = QMenuBar(self)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openInput)
        fileMenu.addAction(openTarget)
        fileMenu.addAction(exitAct)
        
        self.setWindowTitle(self.title)
        self.setContentsMargins(0,39,0,0)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        button = QPushButton('Create triangulation', self)
        button2 = QPushButton('Morph', self)
        button.move(0,20)
        button2.move(104,20)
        screenShape = QDesktopWidget().screenGeometry()
        width = screenShape.width()
        button.resize(104,25)
        button2.resize(50,25)
        button.setStyleSheet("Text-align:center");
        button2.setStyleSheet("Text-align:center");
        button.clicked.connect(self.triangulation) 
        button2.clicked.connect(self.morph)   
        self.show()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Morph()
    sys.exit(app.exec_())
