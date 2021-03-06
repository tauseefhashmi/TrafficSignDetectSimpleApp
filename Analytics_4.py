# -*- coding: utf-8 -*-
"""Analytics_4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1we7KBPqdA6whltyplBHb24AsA4y4IEPo

# Traffic Sign Detection Model using EfficientNet

###Import the Libraries and Functions.
"""

#Connect/Mount to Google Drive
from google.colab import drive
drive.mount('/gdrive')

#Install all the Libraries
!pip install keras
!pip install tensorflow
!pip install pandas 
!pip install sklearn 
!pip install matplotlib
!pip install fastapi
!pip install python-multipart

#Import all the required packages.
import os 
import zipfile
import tensorflow
import tensorflow as tf 
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras import layers 
from tensorflow.keras import Model 
import matplotlib.pyplot as plt
from zipfile import *
from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling2D
import numpy
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from PIL import Image
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout

"""### Unzip the Dataset zip File in Google Drive and Load the Data."""

# !unzip -q "Source Path of the Zip File" -d "Destination Path of where file needs to be Unzipped."
!unzip -q /content/drive/MyDrive/GoogleCollabWork/Traffic.zip -d /content/drive/MyDrive/GoogleCollabWork/Traffic1

"""### TIME CONSUMING PROCESSING OF IMAGES AND LABELLING THEM"""

#Label all the Images of the Dataset
image_data = []
image_labels = []
total_classes = 43
height = 64
width = 64
channels = 3
#Enter the path where the zip file is extracted.
input_path = '/content/drive/MyDrive/GoogleCollabWork/Traffic1'

for i in range(total_classes):
    path = input_path + '/Train/' + str(i)
    print(path)
    images = os.listdir(path)

    for img in images:
        try:
            image = cv2.imread(path + '//' + img)
            image_fromarray = Image.fromarray(image, 'RGB')
            resize_image = image_fromarray.resize((height, width))
            image_data.append(np.array(resize_image))
            image_labels.append(i)
        except:
            print("Error - Image loading")

"""####Converting lists into numpy arrays"""

#Converting lists into numpy arrays
image_data = numpy.array(image_data)
image_labels = numpy.array(image_labels)

#Checking the Default Images of all the 43 Classes.
plt.figure(figsize=(10, 10))
for i in range (0,43):
    plt.subplot(7,7,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    path = input_path + "/meta/{0}.png".format(i)
    img = plt.imread(path)
    plt.imshow(img)
    plt.xlabel(i)

"""####shuffling data"""

#shuffling data
shuffle_indexes = np.arange(image_data.shape[0])
np.random.shuffle(shuffle_indexes)
image_data = image_data[shuffle_indexes]
image_labels = image_labels[shuffle_indexes]

"""###Splitting training and testing dataset"""

#Splitting training and testing dataset
X_train, X_valid, y_train, y_valid = train_test_split(image_data, image_labels, test_size=0.2, random_state=42, shuffle=True)

#X_train = X_train/255 
#X_valid = X_valid/255

print("X_train.shape", X_train.shape)
print("X_valid.shape", X_valid.shape)
print("y_train.shape", y_train.shape)
print("y_valid.shape", y_valid.shape)

#Converting the labels into one hot encoding
y_train = tensorflow.keras.utils.to_categorical(y_train, total_classes)
y_valid = tensorflow.keras.utils.to_categorical(y_valid, total_classes)
print(y_train.shape)
print(y_valid.shape)

"""# Modelling

## EfficientNet B7
"""

from tensorflow.keras.applications import EfficientNetB7
model = EfficientNetB7(input_shape = (64, 64, 3), include_top = False, weights = 'imagenet')

# Untraining existing weights
for layer in model.layers:
    layer.trainable = False

x = model.output
x = layers.Flatten()(x)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dropout(0.5)(x)
predictions = layers.Dense(y_train.shape[1], activation="softmax")(x)
model_final = Model(model.input, predictions)

"""###B7 Model using Adam Optimizer LR=0.0001 and Decay=1e-6"""

model3_final=model2_final

model3_final.compile(tensorflow.keras.optimizers.Adam(learning_rate=0.0001, decay=1e-6),loss='binary_crossentropy',metrics=['accuracy'])

eff3_history = model3_final.fit(x=X_train,y=y_train,batch_size=64, validation_data =(X_valid, y_valid), steps_per_epoch = 150, epochs = 20)

#Save The Model
model3_final.save("B7ModelusingAdamOptimizerLRandDecay.h5")

"""### B7 with RMSprop Optimizer LR=0.0001 and Decay=1e-6"""

model2_final=model_final

model_final.compile(optimizer=tensorflow.keras.optimizers.RMSprop(learning_rate= 0.0001,decay=1e-6),loss='binary_crossentropy',metrics=['accuracy'])

eff_history = model_final.fit(x=X_train,y=y_train,batch_size=64, validation_data =(X_valid, y_valid), steps_per_epoch = 100, epochs = 20)

### Save the Model
model_final.save("B7withRMSpropOptimizer.h5")

"""## EfficientNetB0 """

from tensorflow.keras.applications import EfficientNetB0
model = EfficientNetB0(input_shape = (64, 64, 3), include_top = False, weights = 'imagenet')

# Untraining existing weights
for layer in model.layers:
    layer.trainable = False

x = model.output
x = layers.Flatten()(x)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dropout(0.5)(x)
predictions = layers.Dense(y_train.shape[1], activation="softmax")(x)
model_final = Model(model.input, predictions)

"""### B0  Model using Adam Optimizer LR=0.0001 and Decay=1e-6"""

model2_final=model_final

model_final.compile(optimizer=tensorflow.keras.optimizers.Adam(learning_rate= 0.0001),loss='binary_crossentropy',metrics=['accuracy'])

eff_history = model_final.fit(x=X_train,y=y_train,batch_size=64, validation_data =(X_valid, y_valid), steps_per_epoch = 100, epochs = 15)

#Save the Model
model_final.save("B0ModelusingAdamOptimizerLRandDecay.h5")

"""###BO Model with RMSprop optimizer LR=0001 and Decay=1e-6"""

model3_final=model2_final

model2_final.compile(tensorflow.keras.optimizers.RMSprop(learning_rate=0.0001, decay=1e-6),loss='binary_crossentropy',metrics=['accuracy'])

eff2_history = model2_final.fit(x=X_train,y=y_train,batch_size=64, validation_data =(X_valid, y_valid), steps_per_epoch = 100, epochs = 15)

###Save the Model
model2_final.save("B0withRMSProp.h5")

"""##PLOT THE GRAPHS"""

#Here Enter the Variable in which the Model.fit was stored.
history=eff3_history ##<<==KINDLY PUT THE VARIABLE INPLACE OF eff3_history

#plotting graphs for Accuracy of The Model 
plt.figure(0)
plt.plot(history.history['accuracy'], label='training accuracy')
plt.plot(history.history['val_accuracy'], label='validation accuracy')
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()
plt.figure(1)
plt.plot(history.history['loss'], label='training loss')
plt.plot(history.history['val_loss'], label='validation loss')
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.show()

pd.DataFrame(eff_history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1) # setting limits for y-axis
plt.show()

"""### Dictionary to Label all the Classes"""

classes = { 1:'Speed limit (20km/h)',
            2:'Speed limit (30km/h)', 
            3:'Speed limit (50km/h)', 
            4:'Speed limit (60km/h)', 
            5:'Speed limit (70km/h)', 
            6:'Speed limit (80km/h)', 
            7:'End of speed limit (80km/h)', 
            8:'Speed limit (100km/h)', 
            9:'Speed limit (120km/h)', 
            10:'No passing', 
            11:'No passing veh over 3.5 tons', 
            12:'Right-of-way at intersection', 
            13:'Priority road', 
            14:'Yield', 
            15:'Stop', 
            16:'No vehicles', 
            17:'Veh > 3.5 tons prohibited', 
            18:'No entry', 
            19:'General caution', 
            20:'Dangerous curve left', 
            21:'Dangerous curve right', 
            22:'Double curve', 
            23:'Bumpy road', 
            24:'Slippery road', 
            25:'Road narrows on the right', 
            26:'Road work', 
            27:'Traffic signals', 
            28:'Pedestrians', 
            29:'Children crossing', 
            30:'Bicycles crossing', 
            31:'Beware of ice/snow',
            32:'Wild animals crossing', 
            33:'End speed + passing limits', 
            34:'Turn right ahead', 
            35:'Turn left ahead', 
            36:'Ahead only', 
            37:'Go straight or right', 
            38:'Go straight or left', 
            39:'Keep right', 
            40:'Keep left', 
            41:'Roundabout mandatory', 
            42:'End of no passing', 
            43:'End no passing veh > 3.5 tons' }

"""#COMPARING WITH VGG"""

#Splitting training and testing dataset
X_train, X_valid, y_train, y_valid = train_test_split(image_data, image_labels, test_size=0.2, random_state=42, shuffle=True)

X_train = X_train/255 
X_valid = X_valid/255

print("X_train.shape", X_train.shape)
print("X_valid.shape", X_valid.shape)
print("y_train.shape", y_train.shape)
print("y_valid.shape", y_valid.shape)

#Converting the labels into one hot encoding
y_train = tensorflow.keras.utils.to_categorical(y_train,)
y_valid = tensorflow.keras.utils.to_categorical(y_valid,)
print(y_train.shape)
print(y_valid.shape)

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model

base_model = VGG16(input_shape = (64, 64, 3), # Shape of our images
include_top = False, # Leave out the last fully connected layer
weights = 'imagenet')

for layer in base_model.layers:
    layer.trainable = False

# Flatten the output layer to 1 dimension
x = layers.Flatten()(base_model.output)

# Add a fully connected layer with 512 hidden units and ReLU activation
x = layers.Dense(512, activation='relu')(x)

# Add a dropout rate of 0.5
x = layers.Dropout(0.5)(x)

# Add a final sigmoid layer for classification
x = layers.Dense(1, activation='sigmoid')(x)

model = tf.keras.models.Model(base_model.input, x)

model.compile(optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.0001), loss = 'binary_crossentropy',metrics = ['acc'])

tf.config.experimental_run_functions_eagerly(True)

vgghist = model.fit(X_train, y_train, batch_size=128, epochs=3,validation_data=(X_valid, y_valid))

"""## CODE FOR THE WEB APP only For Cloud Deployment"""

import os
cwd = os.getcwd()
print(cwd)

from tensorflow.keras.models import load_model
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import shutil

model = load_model('Traffic_classifier.h5')
app = FastAPI()


def detect(img):
  classes = { 1:'Speed limit (20km/h)',
            2:'Speed limit (30km/h)', 
            3:'Speed limit (50km/h)', 
            4:'Speed limit (60km/h)', 
            5:'Speed limit (70km/h)', 
            6:'Speed limit (80km/h)', 
            7:'End of speed limit (80km/h)', 
            8:'Speed limit (100km/h)', 
            9:'Speed limit (120km/h)', 
            10:'No passing', 
            11:'No passing veh over 3.5 tons', 
            12:'Right-of-way at intersection', 
            13:'Priority road', 
            14:'Yield', 
            15:'Stop', 
            16:'No vehicles', 
            17:'Veh > 3.5 tons prohibited', 
            18:'No entry', 
            19:'General caution', 
            20:'Dangerous curve left', 
            21:'Dangerous curve right', 
            22:'Double curve', 
            23:'Bumpy road', 
            24:'Slippery road', 
            25:'Road narrows on the right', 
            26:'Road work', 
            27:'Traffic signals', 
            28:'Pedestrians', 
            29:'Children crossing', 
            30:'Bicycles crossing', 
            31:'Beware of ice/snow',
            32:'Wild animals crossing', 
            33:'End speed + passing limits', 
            34:'Turn right ahead', 
            35:'Turn left ahead', 
            36:'Ahead only', 
            37:'Go straight or right', 
            38:'Go straight or left', 
            39:'Keep right', 
            40:'Keep left', 
            41:'Roundabout mandatory', 
            42:'End of no passing', 
            43:'End no passing veh > 3.5 tons' }
  image = Image.open((img))
  image = image.resize((64,64))
  image = np.expand_dims(image, axis=0)
  detect_list = np.array(image)
  pred = model.predict([detect_list])[0]
  pred = np.argmax(pred)
  prediction = classes[int(pred)+1]
  return prediction

@app.post('/detect_sign')
def root(file: UploadFile = File(...)):
    with open(file.filename, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    prediction = detect(img=file.filename)
    return {"prediction":prediction}

"""##GUI for the App. ONLY FOR LOCAL MACHINE"""

!pip install tkinter

import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy
from keras.models import load_model

#Load the Model
model = load_model('traffic_classifier.h5')

#initialise GUI
top=tk.Tk(screenName=Hey)
top.geometry('800x600')
top.title('Traffic Sign classification')
top.configure(background='#CDCDCD')
label=Label(top,background='#CDCDCD', font=('arial',15,'bold'))
sign_image = Label(top)
def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((30,30))
    image = numpy.expand_dims(image, axis=0)
    image = numpy.array(image)
    pred1 = model_final.predict([image])[0]
    pred  = numpy.argmax(pred1)
    sign = classes[pred+1]
    print(sign)
    label.configure(foreground='#011638', text=sign) 
def show_classify_button(file_path):
    classify_b=Button(top,text="Classify Image",command=lambda: classify(file_path),padx=10,pady=5)
    classify_b.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
    classify_b.place(relx=0.79,rely=0.46)
def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass
upload=Button(top,text="Upload an image",command=upload_image,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
upload.pack(side=BOTTOM,pady=50)
sign_image.pack(side=BOTTOM,expand=True)
label.pack(side=BOTTOM,expand=True)
heading = Label(top, text="Know Your Traffic Sign",pady=20, font=('arial',20,'bold'))
heading.configure(background='#CDCDCD',foreground='#364156')
heading.pack()
top.mainloop()

"""#FLASK DEPLOYMENT"""

model=load_model('Traffic_classifier.h5')

!pip install -q streamlit

# %%writefile app.py
import streamlit as st
import tensorflow as tf



@st.cache(allow_output_mutation=True)
def load_model():
  model=tf.keras.models.load_model('/content/drive/MyDrive/GoogleCollabWork/Traffic1/traffic_classifier.h5')
  return model
with st.spinner('Model is being loaded..'):
  model=load_model()

st.write("""
         # Traffic Sign Classification
         """
         )

file = st.file_uploader("Please upload an brain scan file", type=["png"])
import cv2
from PIL import Image, ImageOps
import numpy as np
st.set_option('deprecation.showfileUploaderEncoding', False)
def import_and_predict(image_data, model):
    
        size = (64,64)    
        image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
        image = np.asarray(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #img_resize = (cv2.resize(img, dsize=(75, 75),    interpolation=cv2.INTER_CUBIC))/255.
        
        img_reshape = img[np.newaxis,...]
    
        prediction = model.predict(img_reshape)
        
        return prediction
if file is None:
    st.text("Please upload an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    predictions = import_and_predict(image, model)
    score = tf.nn.softmax(predictions[0])
    st.write(prediction)
    st.write(score)
    print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)

!pip install ngrok
!pip install flask_ngrok

from flask import Flask
from flask_ngrok import run_with_ngrok
app = Flask(__name__)
run_with_ngrok(app)   
  
@app.route("/")
def home():
    return root()

from tensorflow.keras.models import load_model
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import shutil

model = load_model('Traffic_classifier.h5')
app2 = FastAPI()


def detect(img):
    # detect_list=[]
    classes = { 1:'Speed limit (20km/h)',
            2:'Speed limit (30km/h)', 
            3:'Speed limit (50km/h)', 
            4:'Speed limit (60km/h)', 
            5:'Speed limit (70km/h)', 
            6:'Speed limit (80km/h)', 
            7:'End of speed limit (80km/h)', 
            8:'Speed limit (100km/h)', 
            9:'Speed limit (120km/h)', 
            10:'No passing', 
            11:'No passing veh over 3.5 tons', 
            12:'Right-of-way at intersection', 
            13:'Priority road', 
            14:'Yield', 
            15:'Stop', 
            16:'No vehicles', 
            17:'Veh > 3.5 tons prohibited', 
            18:'No entry', 
            19:'General caution', 
            20:'Dangerous curve left', 
            21:'Dangerous curve right', 
            22:'Double curve', 
            23:'Bumpy road', 
            24:'Slippery road', 
            25:'Road narrows on the right', 
            26:'Road work', 
            27:'Traffic signals', 
            28:'Pedestrians', 
            29:'Children crossing', 
            30:'Bicycles crossing', 
            31:'Beware of ice/snow',
            32:'Wild animals crossing', 
            33:'End speed + passing limits', 
            34:'Turn right ahead', 
            35:'Turn left ahead', 
            36:'Ahead only', 
            37:'Go straight or right', 
            38:'Go straight or left', 
            39:'Keep right', 
            40:'Keep left', 
            41:'Roundabout mandatory', 
            42:'End of no passing', 
            43:'End no passing veh > 3.5 tons' }
    image = Image.open((img))
    image = image.resize((64,64))
    image = np.expand_dims(image, axis=0)
    detect_list = np.array(image)
    pred = model.predict([detect_list])[0]
    pred = np.argmax(pred)
    prediction = classes[int(pred)+1]
    return prediction
from google.colab import files
uploaded = files.upload()
@app.route('/detect_sign')
def root(file:uploaded):
    with open(file.filename, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    prediction = detect(img=file.filename)
    return {"prediction":prediction}

app.run()