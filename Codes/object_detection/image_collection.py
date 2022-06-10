import cv2
import uuid  #unique identifier, allow to name images uniquely 
import os   #play with path and create folders
import time 

#define images to collect
labels = ['thumbsup', 'thumbsdown', 'thankyou', 'livelong']
number_imgs = 5

#setup folders
base_dir=os.path.dirname(os.path.abspath(__file__)) #to get base path for the py file
images_path = os.path.join(base_dir,'workspace','images','collectedImages') #creates a path
#if done in jupyter notebook then no need to get base dir, it directly takes by default where the ipynb is made.

if not os.path.exists(images_path): #check if path exists
    if os.name == 'posix':       #for linux to check os 
        os.makedirs(images_path) #if no such path exists it recursively creates directory.(in case of jupyter simply !mkdir{})
    if os.name == 'nt':           #for windows to check os
        os.makedirs(images_path)
for label in labels:
    path = os.path.join(images_path, label)
    if not os.path.exists(path):
        os.mkdir(path) #if no such path exists it creates directory.(in case of jupyter simply !mkdir{})

#capturing images
for label in labels:
    cap=cv2.VideoCapture(0)
    print('collecting images for {}'.format(label)) #more elegant way of cancatenating a string
    time.sleep(10)
    for imgs in range(number_imgs):
        print("Collecting image {}".format(imgs))
        ret, frame = cap.read()
        imgname=os.path.join(images_path,label,label+'{}.jpg'.format(str(uuid.uuid1())))#uuid gives unique random no.
        cv2.imwrite(imgname,frame)
        cv2.imshow('frame',frame)
        time.sleep(3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
        #cv2.waitKey(1) returns the character code of the currently pressed key and -1 if no key is pressed. 
        #the & 0xFF is a binary AND operation to ensure only the single byte (ASCII) representation of the key remains,
        #as for some operating systems cv2.waitKey(1) will return a code that is not a single byte. 
        #ord('q') always returns the ASCII representation of 'q' which is 113 (0x71 in hex).
            break
cap.release() #releases the software and hardware resources.
cv2.destroyAllWindos()


