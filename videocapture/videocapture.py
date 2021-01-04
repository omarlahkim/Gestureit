import cv2
from CONSTANTS import *
from Utils.FramesStore import FramesStore

"""
------------------------------------------------------------------------------------------------------------------------
Video Capture Class
------------------------------------------------------------------------------------------------------------------------
Utility:
Video Capture is the class that implements all the computer vision needed functions to display and gather images 
used in the project.  
------------------------------------------------------------------------------------------------------------------------
Declaration:
Takes in arguments the mode, which is by default 0 that means the video capture mode from default camera, 
could be also a path to an image

------------------------------------------------------------------------------------------------------------------------
Work Flow:
- Instanciate a Video Capture object
- Update image by using method: update()
- Add a text by using method addRightText() or addLeftText()
If you want to have other frames that takes a certain zone of the main frame:
    - Add frame by using method addFrame()
- Display the frames by using method display()
- Dont forget to releaseCamera and cv2.destryAllWindows()   
For a live camera capture:
- Implement it in a while loop with an fps
------------------------------------------------------------------------------------------------------------------------
"""


class videoCapture:
    def __init__(self, mode=0):
        self.capture = cv2.VideoCapture(0)
        self.__running = True
        self.frame = cv2.flip(self.getMainFrame(), 1)
        self.__views = FramesStore()
        self.__RightTexts = []
        self.__LeftTexts = []
        self.__rightXPosition = RIGHT_TEXT_X
        self.__rightYPosition = 100
        self.__LeftXPosition = LEFT_TEXT_X
        self.__LeftYPosition = 100
        self.__capture_mode = mode

    def isRunning(self):
        return self.__running

    def getMainFrame(self):
        s, frame = self.capture.read()
        if s:
            pass
        return frame

    def addFrame(self, name, x1, x2, y1, y2, color=(39, 174, 96), borderSize=3):
        regionFrame = self.frame[x1:x2, y1:y2]
        if name not in self.__views.getFramesNames():
            self.__views.addFrame(regionFrame, name, x1, x2, y1, y2)

        else:
            # print("Please choose another name, this one is already taken!")
            pass
        cv2.rectangle(self.frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1),
                      color,
                      borderSize)

    def addRightText(self, text, font=cv2.FONT_HERSHEY_PLAIN, scale=TEXT_SCALE, color=COLOR_WHITE, weight=TEXT_WEIGHT):
        if len(self.__RightTexts) >= 1:
            prevText = self.__RightTexts[-1]
            self.__rightYPosition = prevText["y"]
            self.__rightYPosition += 50
        self.__RightTexts.append(
            {"text": text, "x": self.__rightXPosition, "y": self.__rightYPosition, "font": font, "scale": scale,
             "color": color, "weight": weight})

    def addLeftText(self, text, font=cv2.FONT_HERSHEY_PLAIN, scale=TEXT_SCALE, color=COLOR_WHITE, weight=TEXT_WEIGHT,id=False):
        if len(self.__LeftTexts) >= 1:
            prevText = self.__LeftTexts[-1]
            self.__LeftYPosition = prevText["y"]
            self.__LeftYPosition += 50
        if id>=1:
            count = 0
            for txt in self.__LeftTexts:
                count +=1
                if id == txt['id']:
                    self.__LeftTexts[count] ={"text": text, "x": self.__LeftXPosition, "y": self.__LeftYPosition, "font": font, "scale": scale,
             "color": color, "weight": weight,"id":id}

        self.__LeftTexts.append(
            {"text": text, "x": self.__LeftXPosition, "y": self.__LeftYPosition, "font": font, "scale": scale,
             "color": color, "weight": weight,"id":id})

    def displayRegion(self, regionName):
        if (regionName in self.__views.getFramesNames()):
            region = self.__views.getFrame(regionName)
            mainFrame = self.getMainFrame()
            region.updateFrameRegion(mainFrame)
            cv2.imshow(regionName, self.getFrameRegion(regionName))

        else:
            print("The following region does not exist, please add it first!")

    def getFrame(self, regionName):
        return self.__views.getFrame(regionName)

    def displayFrames(self):
        for frame in self.__views.getFramesNames():
            self.displayRegion(frame)

    def displayMain(self):
        frame = self.frame
        cv2.imshow("Main", frame)

    def stop(self):
        self.__running = False

    def releaseCamera(self):
        self.capture.release()

    def displayRightTexts(self):
        Texts = self.__RightTexts
        mainFrame = self.frame
        for i in range(len(Texts)):
            TextObject = Texts[i]
            cv2.putText(mainFrame, TextObject['text'], (TextObject['x'], TextObject['y']), TextObject['font'],
                        TextObject['scale'], TextObject['color'], TextObject['weight'])
            self.updateMainFrame(mainFrame)

    def displayLeftTexts(self):
        Texts = self.__LeftTexts
        mainFrame = self.frame
        for i in range(len(Texts)):
            TextObject = Texts[i]
            cv2.putText(mainFrame, TextObject['text'], (TextObject['x'], TextObject['y']), TextObject['font'],
                        TextObject['scale'], TextObject['color'], TextObject['weight'])
            self.updateMainFrame(mainFrame)

    def getFrameRegion(self, name):
        return self.__views.getFrame(name).getFrameRegion()

    def update(self):
        self.frame = self.getMainFrame()
        self.__RightTexts = []
        self.__LeftTexts = []
        self.__rightXPosition = 30
        self.__rightYPosition = 100

    def updateMainFrame(self, frame):
        self.frame = frame

    def display(self):
        self.displayLeftTexts()
        self.displayRightTexts()
        self.displayMain()
        self.displayFrames()
