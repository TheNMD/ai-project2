import cv2
import numpy as np

def mse(img1, img2):
   h, w = img1.shape
   diff = cv2.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

img1 = cv2.imread('sample1.jpg')
img2 = cv2.imread('sample01.jpg')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

print(img1.shape)

error = mse(img1, img2)

print("Image matching Error between the two images:",error)