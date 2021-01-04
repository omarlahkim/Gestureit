import shutil, os, time
from trainer import Trainer
from predictor import Predictor
from Collector import Collector
from videocapture.videocapture import videoCapture
from layers import CNN_LAYERS
import cv2
from Utils.filesCounter import filesCounter
from keras.models import model_from_json
from art import *
from colorit import *
from Utils.ResettableTimer import ResettableTimer
from Gestures import Gestures
from Commands import Commands

"""
------------------------------------------------------------------------------------------------------------------------
GESTURES TO ACTIONS PROJECT
Authors: Soufiane KARROUMI & Omar LAHKIM
------------------------------------------------------------------------------------------------------------------------
Purpose:

This project is using Computer Vision, Machine Learning, and to be more specific Deep Learning to detect hand gestures,
and convert them to actions on the computer. 
This could be useful for people who can't stand up to reach the computer's mouse or keyboard to some actions such as 
increasing the volume, descreasing it, or even shutting down their computers. 
Could be also used in the medical sector, lets suppose a sick person who can't speak and needs help in a Hospital, this 
application could help him/her to call for help just with a simple gesture.
------------------------------------------------------------------------------------------------------------------------
Future Improvements:

This implementation supports only one hand gesures detection, but it can be optimized and improved to be used on 2 hands
gestures! By using threading, and assigning a thread for each hand gesture recogntion.
------------------------------------------------------------------------------------------------------------------------
Work Flow:

Here we have different functions, but most of them are for handling display and user inputs.
The most important ones are: 
clean(): Implements the logic for cleaning the project from any training data created/generated and clear the model. 
collect_data(mode): Implements the logic for collecting training and test data.
train(): Implements the logic for training the model.
run(): Implements the logic for starting the predictions.
listenForEvent(): Implements the logic for listening for a gesture in order to convert it into action
executeAction(): implements the logic for running the action thrigered by the listener. 
------------------------------------------------------------------------------------------------------------------------
Instructions:

- Main Libraries used: 
    Computer Vision: Opencv
    Deep Learning/Machine learning: Tensorflow but on top of it Keras 
    (Versions are available in requirements.txt)
- Python Version tested and approved: Python 3.6
- Install Needed Modules:
    Working Directory: Project Folder
    pip3 install -r requirements.txt
- python main.py
Using the interface:
    - Everything is explained on runtime in the cmd
------------------------------------------------------------------------------------------------------------------------
Algorithms & Data Structures:

- We first created some custom implementations as classes for each feature such as the Predictor, and Video Capture...
in order to have better scalability on the other implementations and be able to add different functionnalities easily 
such as the 2 hands gesture recognitions just by adding a multi threading to the project. 
- We used mainly Array, but more often Dictionnaries and JSON to manage data in our project.
- We created a custom implementation to manage frames storing (Utils/FramesStore), because dictionnaries only hold 
some specific types of data, such as integers,and strings... and the frame implementation in opencv is an object.
- We created a custom implementation of a Timer to be able to reset it whenever we want, the default implementation 
doesn't allow it.
- We mainly put all the necessary helping functions and classes in Utils folder.
- model folder holds the model.
- data folder holds the training and test data.
- scripts folder holds all the "apple script" scripts used for the commands/actions execution in MACOS.
- videocapture folder holds the class file that implements the custom implementation of cv2.
- Config folder takes the configurations such as the gestures implemented in the project.     
- layers file holds the layers used in the model.
- More detailed documentation is provided as a PDF with the project, and each class has its documentation in its 
specific file.
- A more detailed explanation about how things work behind the scenes is provided in a separate document with the project.
------------------------------------------------------------------------------------------------------------------------
"""

g = Gestures()
gestures = g.getGestures()

commands = Commands()

#Action execution
def executeAction():
    global Prediction
    if Prediction:
        predictedGesture = str(g.getGestureIndex(Prediction))
        commands.executeCommand(predictedGesture)
        os.system('say beep')
        time.sleep(5)


counter = 1
Prediction = False
timer = ResettableTimer(5, executeAction)
mode = True
prev = 'ZERO'
modes = {0: 'clean', 1: 'collect', 2: 'train', 3: 'predict', 4: 'exit'}

#Action listener
def listenForEvent(actual):
    global prev
    global timer
    global counter
    if prev == actual:
        if timer == 60:
            executeAction()

    else:
        prev = actual
        counter = 0
        timer.reset()


# organize frame coordinates
def ROIcoordinates(frame):
    x1 = 50
    y1 = 50
    x2 = int(0.5 * frame.shape[1])
    y2 = int(0.5 * frame.shape[1])
    return (x1, x2, y1, y2)


# load model
def loadedModel():
    # Loading the model
    json_file = open("model/model-bw.json", "r")
    model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(model_json)
    # load weights into new model
    loaded_model.load_weights("model/model-bw.h5")
    return loaded_model


# Training mode
def train():
    trainer = Trainer()
    trainer.addLayers(CNN_LAYERS)
    trainer.compileClassifier()
    trainingData = trainer.trainingImagesAugmentation('data/train')
    testingData = trainer.testingImagesAugmentation('data/test')
    trainer.train(trainingData, testingData)
    trainer.save('model/')


# data collecting mode
def collect_data(mode):
    video = videoCapture()
    collector = Collector(mode)
    directory = collector.getDirectory()
    frame = video.getMainFrame()
    ROI_NAME = 'Region of Interest'
    print(color("Data collecting started...", Colors.yellow))
    print(color("video windows is opening ", Colors.yellow))
    collector.generateFolders()
    while video.isRunning():
        video.update()
        # Add Texts and Frames
        video.addRightText(mode)
        for gesture in gestures:
            video.addRightText(gestures[gesture] + ': ' + str(filesCounter(directory + str(gesture))[0]))
        video.addFrame(ROI_NAME, ROIcoordinates(frame)[0], ROIcoordinates(frame)[1], ROIcoordinates(frame)[2],
                       ROIcoordinates(frame)[3])
        video.display()
        interrupt = cv2.waitKey(10)
        ROI = video.getFrameRegion(ROI_NAME)
        collector.keyPressToImage(ROI, interrupt)
        if interrupt & 0xFF == 27:
            video.stop()
    video.releaseCamera()
    cv2.destroyAllWindows()
    print(color("Data collecting finished", Colors.yellow))


# prediction mode
def run():
    print(color("Prediction mode started...", Colors.yellow))
    # loading camera video
    video = videoCapture()
    loaded_model = loadedModel()
    print("model loaded successfully...")
    predictor = Predictor(loaded_model, gestures)
    frame = video.getMainFrame()
    ROI_NAME = 'Region of Interest'
    Red = 39
    Green = 174
    Blue = 96

    while video.isRunning():
        global counter
        counter += 1
        video.update()
        # Add Texts, Frames, and Logic ---------------------------------------------------------------------------------
        video.addFrame(ROI_NAME, ROIcoordinates(frame)[0], ROIcoordinates(frame)[1], ROIcoordinates(frame)[2],
                       ROIcoordinates(frame)[3])
        ROI = video.getFrameRegion(ROI_NAME)
        prediction = predictor.predict(ROI)
        global Prediction
        listenForEvent(prediction)
        video.addRightText(prediction)
        gestIndex = g.getGestureIndex(prediction)
        commandName = commands.commandName(commands.getCommandByGesture(gestIndex))
        if counter > 0:
            Red = int((Red + counter // 15)) % 255
        else:
            Red = 39
        Green = (Green) % 255
        DynamicColor = (Red, Green, Blue)
        video.addLeftText(commandName, color=DynamicColor)

        # ---------------------------------------------------------------------------------------------------------------
        video.display()
        Prediction = prediction
        interrupt = cv2.waitKey(10)
        if interrupt & 0xFF == 27:
            video.stop()

    video.releaseCamera()
    cv2.destroyAllWindows()
    print(color("Prediction finished...", Colors.yellow))

#rename a gesture
def replaceGesture(index, name):
    g.renameGesture(index, name)

#clean model and data
def clean():
    print(color("Cleaning started...", Colors.yellow))
    try:
        shutil.rmtree('data')
        shutil.rmtree('model')
        os.mkdir('model')
        time.sleep(2)
        print(color("Cleaning finished.", Colors.yellow))
    except:

        pass


# USER FRIENDLY PRINTS
def printWelcome():
    print(color('Welcome to our program that translates your hand gestures to actions on your computer', Colors.orange))
    print(color('Please read the instructions below: ', Colors.orange))


def displayGestures():
    print(color("AVAILABLE GESTURES:", Colors.yellow))
    for gesture in gestures:
        print(color("{}: {}".format(gestures[gesture], str(gesture)), Colors.yellow))


def printInstructions():
    print(color("AVAILABLE GESTURES:", Colors.yellow))
    for gesture in gestures:
        print(color("{}: {}".format(gesture, gestures[gesture]), Colors.yellow))


def printMainOptions():
    print(color(" choose ", Colors.green))
    menu = {"REPLACE_GESTURE": 0, "COLLECT_IMAGES": 1, "TRAIN_MODEL": 2, "START_PREDICTIONS": 3}
    for item in menu:
        print(color("{}: {}".format(item, menu[item]), Colors.yellow))


def replaceGestureOptions():
    displayGestures()
    gesture_index = int(input(color('Please choose the gesture to be replaced: ', Colors.orange)))
    name = str(input(color('Please give a name to your new gesture: ', Colors.orange)))
    replaceGesture(gesture_index, name)


def collectDataOptions():
    print(color("Collecting data modes: ", Colors.yellow))
    print(color("{}: {}".format("train", "0"), Colors.yellow))
    print(color("{}: {}".format('test', "1"), Colors.yellow))
    mode = str(input(color('Please choose a mode for your data collection: ', Colors.orange)))
    if mode == str(0) or mode == 'train':
        collect_data('train')
    elif mode == str(1) or mode == 'test':
        collect_data('test')
    else:
        print(color('Please choose an available mode.', Colors.yellow))
        pass


def printModes(modes):
    print(color("The following are the available modes", Colors.yellow))
    for mode in modes:
        print(color("{}: {}".format(modes[mode], mode), Colors.yellow))


def handleModes(mode):
    if mode != True:
        if mode == 'clean' or mode == str(0):
            clean()
        elif mode == 'collect' or mode == str(1):
            collectDataOptions()
        elif mode == 'train' or mode == str(2):
            train()
        elif mode == 'predict' or mode == str(3):
            commands.printCommands()
            run()
        else:
            print("Please choose one of the available modes.")
            pass


if __name__ == '__main__':
    tprint('GESTUREIT')
    aprint("happy")
    print(color("Hand Gestures to Actions .", Colors.purple))
    aprint("happy")
    print()
    printWelcome()
    while mode != 'exit':
        printModes(modes)
        mode = str(input(color('Please choose a mode: ', Colors.orange)))
        print(mode)
        handleModes(mode)
