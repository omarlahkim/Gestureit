import os
import cv2
from Gestures import Gestures

"""
------------------------------------------------------------------------------------------------------------------------
Data (Images) Collector Class
------------------------------------------------------------------------------------------------------------------------
Utility:

Collector is a class that implement the most import methods to collect, capture and save images in order to train 
the model.

------------------------------------------------------------------------------------------------------------------------
Declaration:
Takes in argument the mode which could be train, or test (collect data for training or test)

------------------------------------------------------------------------------------------------------------------------
Work Flow:
- Instanciate Collector class
- Generate the folders for data (if not already created) using method generateFolders()
- Save Captures using method keyPressToImage() takes the frame and the keypress listener
For live implementation:
Implement it in Video Capture loop
------------------------------------------------------------------------------------------------------------------------
"""
g = Gestures()
gestures = g.getGestures()


class Collector:
    def __init__(self, mode='train'):
        self.__mode = mode
        self.__directory = 'data/' + mode + '/'

    # Create the directory structure
    def generateFolders(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            os.makedirs("data/train")
            os.makedirs("data/test")
            for gesture in gestures:
                os.makedirs("data/train/" + str(gesture))
                os.makedirs("data/test/" + str(gesture))

    def getDirectory(self):
        return self.__directory

    def keyPressToImage(self, frame, interrupt):

        for i in range(len(gestures)):
            if interrupt & 0xFF == ord(str(i)):
                cv2.imwrite(
                    self.__directory + str(i) + '/' + str(len(os.listdir(self.__directory + "/" + str(i)))) + '.jpg',
                    frame)
