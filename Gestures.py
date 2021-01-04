import json




json_file = open("Config/gestures.json", "r")
model_json = json_file.read()
json_file.close()


"""
------------------------------------------------------------------------------------------------------------------------
Gestures Class
------------------------------------------------------------------------------------------------------------------------
Utility:

Gestures is a class that abstracts the implementation of Gestures predicted.

------------------------------------------------------------------------------------------------------------------------
Declaration:

Takes not argument. But fetches the gestures json file in Config folder 

------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------
"""

class Gestures:
    def __init__(self):
        self.__gestures = {}
    def updateGesturesFromJSON(self):
        json_file = open("Config/gestures.json", "r")
        gestures = json_file.read()
        self.__gestures = json.loads(gestures)
        json_file.close()
    def getGestures(self):
        self.updateGesturesFromJSON()
        return self.__gestures
    def renameGesture(self,gesture,name):
        self.updateGesturesFromJSON()
        self.__gestures[str(gesture)] = name
        with open('Config/gestures.json', 'w') as file:
            json.dump(self.__gestures, file, indent=2)

    def getGestureIndex(self,gestureName):
        for gesture in self.__gestures:
            if self.__gestures[gesture] == gestureName:
                return gesture
















