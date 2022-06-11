#import tensorflow as tf
import cv2
import os
import numpy as np

img_array = []
img_dir = 'images'

for i in os.listdir(img_dir):
	img_category = os.path.join(img_dir, i)
	if not os.path.isfile(img_category):
		for j in os.listdir(img_category):
			img_path = os.path.join(img_category, j)
			img = cv2.imread(img_path, cv2.IMREAD_COLOR)
			img = cv2.resize(img, (320,320))
			cv2.imwrite(img_path, img)
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			img_array.append(img)
cv2.destroyAllWindows()

img_array = np.array(img_array)