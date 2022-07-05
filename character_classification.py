# -*- coding: utf-8 -*-
"""Character_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aVMbDNcBFSZvFzNuCvRRt836aCHLCFq7
"""

from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf

# Import TensorFlow Datasets
import tensorflow_datasets as tfds
# Helper libraries
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import logging
logging.basicConfig(level=logging.ERROR) #would show only error and critical, no warnings, debug or info

"""## **Import Dataset**"""

dataset, info = tfds.load('emnist', as_supervised=True, with_info=True, try_gcs=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

character = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

"""## **Explore the data**"""

num_train_examples = info.splits['train'].num_examples #number of examples in the dataset.
num_test_examples = info.splits['test'].num_examples
print("Number of training examples: {}".format(num_train_examples))
print("Number of test examples:     {}".format(num_test_examples))

"""##**Split training data to get validation data**"""

train_split = 0.8
train_size = int(num_train_examples*train_split)
validation_size = num_train_examples-train_size

train_dataset = train_dataset.shuffle(num_train_examples)

train_dataset = train_dataset.take(train_size)
validation_dataset = train_dataset.skip(train_size).take(validation_size)

"""## **Pre-Process the Data**"""

def normalize(images, labels):
  images = tf.cast(images, tf.float32) #converts integer pixel value into float32
  images /= 255
  return images, labels

# The map function applies the normalize function to each element in the train
# and test datasets
train_dataset =  train_dataset.map(normalize)
validation_dataset = validation_dataset.map(normalize)
test_dataset  =  test_dataset.map(normalize)

# The first time you use the dataset, the images will be loaded from disk
# Caching will keep them in memory, making training faster
train_dataset =  train_dataset.cache()
validation_dataset = validation_dataset.cache()
test_dataset  =  test_dataset.cache()

"""## **Explore the processed data**"""

# Take a single image, and remove the color dimension by reshaping
for image, label in test_dataset.take(1):
  break
image = image.numpy().reshape((28,28))#making it an array of 28x28 from simple list of 28x28 no.s btw 0-255(shaping the array without changing any data)

# Plot the image
plt.imshow(image, cmap=plt.cm.binary)#cvts into gray scale and is shown
plt.colorbar()#shows color bar
plt.grid(False) #removes grid boxes in image
plt.show()

plt.figure(figsize=(10,10))
i = 0
for (image, label) in test_dataset.take(25):
    image = image.numpy().reshape((28,28))
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(image, cmap=plt.cm.binary)
    plt.xlabel(character[label])
    i += 1
plt.show()

"""## **CNN Model using tensorflow API**"""

#intuitive understanding of why only these layers??
#xavier or glorot uniform??
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), padding='same', activation=tf.nn.relu, input_shape=(28, 28, 1)), #output having 32 nodes with eaxch of size 28x28x1
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2, 2), strides=2),#output 32 nodes having size 14x14x1 (no exxtra parameters)
    tf.keras.layers.Conv2D(64, (3,3), padding='same', activation=tf.nn.relu),#output 64 nodes having size 14x14x1
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2, 2), strides=2),#output 64 nodes having size 7x7x1 (no exxtra parameters)
    tf.keras.layers.Flatten(),#layer is flattend to give 64x7x7x1 node each of 1 pixel
    tf.keras.layers.Dense(256, activation=tf.nn.relu),#above is connected in dense to give 128 nodes op
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(62, activation=tf.nn.softmax) #above is connected in dense to give 128 nodes op
])

"""## **Model Summary**"""

model.summary()

tf.keras.utils.plot_model(model)

"""## **Compile Model**"""

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

"""## **Train the model**"""

BATCH_SIZE = 32
EPOCHS = 20

train_dataset = train_dataset.cache().repeat().shuffle(train_size).batch(BATCH_SIZE)
test_dataset = test_dataset.cache().batch(BATCH_SIZE)

# train_batches = train_dataset.cache().shuffle(train_size).batch(BATCH_SIZE).prefetch(1)
validation_dataset = validation_dataset.cache().batch(BATCH_SIZE)

history = model.fit(train_dataset, epochs=EPOCHS, verbose=1,steps_per_epoch=math.ceil(train_size/BATCH_SIZE), validation_data=validation_dataset)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(EPOCHS)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

"""## **Accuracy of the model**"""

test_loss, test_accuracy = model.evaluate(test_dataset, steps=math.ceil(num_test_examples/32))
print('Accuracy on test dataset:', test_accuracy)

"""## **Predictions**"""

for test_images, test_labels in test_dataset.take(1):#1 here is 1 batch
  test_images = test_images.numpy()
  test_labels = test_labels.numpy()
  predictions = model.predict(test_images)
  print(predictions.shape)
#shape of predicions is probability of all 62 characters for 32 images(batch size) that is given as input to model.predict.
#np array must be passed inside the predict()

def plot_image(i, predictions_array, true_labels, images):
  predictions_array, true_label, img = predictions_array[i], true_labels[i], images[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  
  plt.imshow(img[...,0], cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)#label with maxm probability
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'
  
  plt.xlabel("{} {:2.0f}% ({})".format(character[predicted_label],
                                100*np.max(predictions_array),
                                character[true_label]),
                                color=color)

i = 12
plt.figure(figsize=(6,3))
plot_image(i, predictions, test_labels, test_images)

model.save('character_classification.h5')