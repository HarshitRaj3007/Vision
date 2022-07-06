# -*- coding: utf-8 -*-
"""Test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ECAHGNxKNw-qUjdAfIM7cJo9FfMDWm9o
"""

from google.colab import drive
drive.mount('/content/drive')

import cv2
import sanjay_drishti as sanjay

img = cv2.imread("sample.png")
#cv2.imshow("image", img)
sanjay.predict(img)

cv2.waitKey(0)
cv2.destroyAllWindows()