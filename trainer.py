# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from Utils.filesCounter import filesCounter

"""
------------------------------------------------------------------------------------------------------------------------
Trainer Class
------------------------------------------------------------------------------------------------------------------------
Utility:
Trainer is class for training our model to be ale to detect the given gestures. 
It works using keras api which is a an API on top of the popular Tensor Flow by Google. 
------------------------------------------------------------------------------------------------------------------------ 
Declaration:
Takes in arguments batch size which is the number of samples generated, 
and epochs which is the number of complete passes through the training dataset.
------------------------------------------------------------------------------------------------------------------------
Work Flow:
- Instanciate Object from the class.
- Add the layers necessary for the training. Method: addLayer(layer)
- Compile the model to declare the optimizer, loss function, and metrics. Method: compileClassifier()
- Apply an Augmentation on the training data set. Method: trainingImagesAugmentation(path) Return: training_data
- Apply an Augmentation on the testing data set. Method: testingImagesAugmentation(path) Return: testing_data
- Start training.  Method: train(training_data,testing_data)
- Save trained model. Method: save(topath)
------------------------------------------------------------------------------------------------------------------------
"""


class Trainer:
    def __init__(self, optimizer=Adam(lr=0.0001), batch_size=3, epochs=13):
        # initiale cnn
        self.__classifier = Sequential()
        # define optimizer used to compile the cnn later
        self.__optimizer = optimizer
        self.__training_size = filesCounter('data/train')[0]
        self.__testing_size = filesCounter('data/test')[0]
        self.__batch_size = batch_size
        self.__steps_per_epoch = self.__training_size -20
        self.__epochs = epochs

    # add layer for cnn
    def addLayer(self, layer):
        self.__classifier.add(layer)
    def addLayers(self,layers):
        for layer in layers:
            self.__classifier.add(layer)

    # compile in order to declare the optimizer, loss function, and metrics
    def compileClassifier(self):
        self.__classifier.compile(optimizer=Adam(lr=0.0001),
                                  loss='categorical_crossentropy',
                                  metrics=['accuracy'])

    # Generating other images from the original ones to have more data for training.
    def trainingImagesAugmentation(self, path):
        # initialize the data generator
        training_data_generator = ImageDataGenerator(rescale=1. / 255,
                                                     shear_range=0.2,
                                                     zoom_range=0.2,
                                                     horizontal_flip=True)
        training_data = training_data_generator.flow_from_directory(path,
                                                                    batch_size=self.__batch_size,
                                                                    # number of samples generated
                                                                    target_size=(225, 225),
                                                                    color_mode='rgb',
                                                                    class_mode='categorical',
                                                                    save_format='jpg',
                                                                    save_prefix='image',
                                                                    )
        return training_data

    # Generating other images from the original ones to have more data for training.
    def testingImagesAugmentation(self, path):
        # initialize the data generator
        testing_data_generator = ImageDataGenerator(rescale=1. / 255)

        testing_data = testing_data_generator.flow_from_directory(path,
                                                                  target_size=(225, 225),
                                                                  batch_size=self.__batch_size,
                                                                  # number of samples generated
                                                                  color_mode='rgb',
                                                                  class_mode='categorical',
                                                                  )
        return testing_data

    def train(self, trainingData, testingData):
        self.__classifier.fit_generator(
            trainingData,
            #steps_per_epoch=self.__steps_per_epoch,  # No of images in training set
            epochs=self.__epochs,  # number of complete passes through the training dataset.
            validation_data=testingData,
            validation_steps=self.__testing_size)  # No of images in test set

    def save(self, path):
        # Saving the model
        model_json = self.__classifier.to_json()
        with open(path + "model-bw.json", "w") as json_file:
            json_file.write(model_json)
        self.__classifier.save_weights(path + 'model-bw.h5')
