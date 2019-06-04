from PIL import Image
import numpy as np
import pylab
import matplotlib.pyplot as plt
import cv2


def calculate_histogram(img):
    hist = np.zeros([256,3], dtype=np.uint32)
    R,C,b = img.shape
    for b in range(3):
        for i in range(0, R):
            for j in range(0, C):
                hist[img[i][j][b],b] += 1
    return hist

def match_histogram(I, J):
    Pj = cdf(J)
    Pi = cdf(I)
    LUT = np.zeros([256,3])
    Gj = 0
    for b in range(3):
        Gj = 0
        for Gi in range(255):
            while Gj < 255 and Pj[Gj,b] <= Pi[Gi,b]:
                Gj = Gj + 1
            LUT[Gi,b] = Gj
    return LUT
    
def cdf(img):
    hist = calculate_histogram(img)
    CDF = np.zeros([256,3])
    for b in range(3):
        for g in range(256):
            CDF[g,b] = np.sum(hist[0:g,b])/np.sum(hist[0:255,b])
    return CDF

def show_histogram(img):
    hist = calculate_histogram(img)
    hist_red = hist[:,0]
    hist_green = hist[:,1]
    hist_blue = hist[:,2]
    bins = np.arange(256)
    plt.subplot(3,1,1)
    plt.bar(bins, hist_red, 1/1.5, align='center', alpha = 0.5, color='r')
    plt.subplot(3,1,2)
    plt.bar(bins, hist_green, 1/1.5, align='center', alpha = 0.5, color='g')
    plt.subplot(3,1,3)
    plt.bar(bins, hist_blue, 1/1.5, align='center', alpha = 0.5, color='b')
    plt.show()
    #pylab.savefig('hist_image1.png', bbox_inches='tight')

def equalize_histogram(img, img1):
    LUT = match_histogram(img,img1)
    red = LUT[:,0]
    green = LUT[:,1]
    blue = LUT[:,2]
    K1 = np.uint8(red[img[:,:,0]])
    K2 = np.uint8(green[img[:,:,1]])
    K3 = np.uint8(blue[img[:,:,2]])
    new_image = np.stack((K1,K2, K3), axis=-1)
    new_image1 = Image.fromarray(new_image)
    new_image1.show()
    return new_image
