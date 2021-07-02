# Crop_Detector

AI CROP DETECTION WEBSITE is mainly used for identifying different crops using the images of their leaves
and classifying them into their respective category or the name of the plant. It can also predict if the 
plant is healthy or if it has any diseases based on the picture given. It has the ability to get the location
of where the image is uploaded, stores all the details along with the image in the database, it has the ability
to show the maps along with coordinates and other details of each image uploaded to the user. It also provides
signup & logins for users and admin to manage their data. Admin also has special access to everything and has
control over the database. It is very much helpful for people who don’t have much information or knowledge on 
different plant varieties and tell if it's healthy or not. Finally, the users have the ability to download all
the reports of previously uploaded content and save them. 

The implementation is done by using Convolutional Neural Networks, in which we collect a dataset of images and
train the images using the principles of CNN like Convolution, MaxPooling, Dense, Flatten, etc. Using a good 
number of epochs along with a suitable batch size and tuning other setting like train_size, etc we get a cnn model.

The obtained model can be used for classifying new images into the different plant categories which are 
previously used for training the model. Using this technique, we are able to get good accuracy and are 
able to predict more precisely when compared to humans. Making the machine do the task reduces the work
of humans and saves time along with good performance.

*See the requirements.txt for all the libraries used.* 

