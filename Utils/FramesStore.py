import cv2


class Frame:
    def __init__(self,frameRegion,name,x1,x2,y1,y2):
        self.__frameName = name
        self.__frameRegion = frameRegion
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

    def getFrameName(self):
        return self.__frameName
    def getFrameRegion(self):
        return self.__frameRegion
    def getX1(self):
        return self.__x1
    def getX2(self):
        return self.__x2
    def getY1(self):
        return self.__y1
    def getY2(self):
        return self.__y2
    def updateFrameRegion(self,mainFrame,size=225):
        frame = mainFrame[self.__x1:self.__x2,self.__y1:self.__y2]
        frame = cv2.resize(frame, (size, size))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.__frameRegion = frame

    def getFrame(self):
        return self.__frameRegion

class FramesStore:
    def __init__(self):
        self.__store = []
    def addFrame(self,frameRegion,name,x1,x2,y1,y2):
        temp = Frame(frameRegion,name,x1,x2,y1,y2)
        self.__store.append(temp)
    def getFrame(self,name):
        for frame in self.__store:
            if (frame.getFrameName() == name):
                return frame
        print('The following frame does not exist, please add it first!')
        return False
    def getFramesNames(self):
        names = []
        for frame in self.__store:
            names.append(frame.getFrameName())
        return names


