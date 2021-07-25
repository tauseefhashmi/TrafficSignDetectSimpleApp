All the Files can be downloaded from https://github.com/tauseefhashmi/TrafficSignDetectSimpleApp
and Dataset from https://www.kaggle.com/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign/download

=====================================================================================


*To run the app just run double click GUI.py or run "python GUI.py" on windows terminal terminal.

IF you want to check the code, than upload the Analytics_4.ipynb file into Google Collab.
*Download the Dataset from "https://www.kaggle.com/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign/download".
*The Downloaded Folder will be in the form of Zip file.
*Upload this Zip file to your Google Drive connected to your Google Collab.

*Mount Drive from Google Colab to Google Drive.
 
*Install all the required libraries: keras,tensorflow,pandas,sklearn,matplotlib,fastapi,python-multipart

*Import all the Packages

*Unzip the Zip file onto Google Drive
using !unzip -q "Source Path of the Zip File" -d "Destination Path of where file needs to be Unzipped."

*Label all the Images of the Dataset.

*Convert the lablelled images into list of numpy array.

*Check all the Default images of all 43 classes in our dataset.

*Perform shuffling of labelled data
*Split data into Training and Testing set in 80:20 ratio.
*Convert the image labels into one hot encoding
*Start Modelling of Your Desired Architecture.
*The best result was of EfficientNetB7 model using Adam Optimizer with Learning Rate=0.0001 and Decay=1e-6
*Steps for modelling
*1.Import the Model from Tensorflow library.
*2.save the model with desired arguments(For our case we used input shape as 64,64,3 and weights='imagenet')
*3.Untrain the existing weights
*4. Compile model with adam optimzers LR and Decay,loss="binary_crossentropy" metrics="accuracy"
*5. Fit the Model with Train and Test Dataset,set epochs as 20 and step per epoch as 150.
*6. Save the values of model.fit in a variable.
*Save the MODEL as "NameOfyourModel.h5" file using model.save("NameOfyourModel.h5") command.You will see a file of same name in left of your colab windows,download it we would need it later
*7.Apply all the above 6 steps same for other models as well.
*Plotting graphs
*Enter the variable where you saved the model.fit() values in history variable.
* just put the hisotry value and plot will be generated using the code

*Labell all the classes of dataset accordingly and save it in Classes dictionary variable.

*Compare with VGG the Dataset apply same 6 steps as in modelling above.

*Code for Web App
*Load the saved model into this app using load_model() function.

*GUI Code for Local Machine
*Load the saved model into this app using load_model() function.

