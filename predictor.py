import operator
import cv2
from keras.utils.vis_utils import plot_model
from Utils.ObjectKeys import getObjectKeys


"""
------------------------------------------------------------------------------------------------------------------------
Predictor Class
------------------------------------------------------------------------------------------------------------------------
Utility:
Predictor is a the class responsible for deploying the prediction mode,
which loads the trained model and predicts the results. 
------------------------------------------------------------------------------------------------------------------------
Declaration:
Takes in arguments the trained mode, and the gestures available. 
------------------------------------------------------------------------------------------------------------------------
Work Flow:
- Load Trained Model
- Instanciate a Predictor Object
- Start Predictions 

For a live predictions:
Implement it in a Video Capture loop
------------------------------------------------------------------------------------------------------------------------
"""

class Predictor:
    def __init__(self,model,gestures):
        self.__model = model
        self.__gestures = gestures
        self.__predictions = {}

    def predict(self,image):
        image = cv2.resize(image, (225, 225))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.reshape(1, 225, 225, 3)
        result = self.__model.predict(image)
        gestures_keys = getObjectKeys(self.__gestures)
        i = 0
        for gesture in gestures_keys:
            self.__predictions[gesture] = result[0][i]
            i+=1
        prediction = sorted(self.__predictions.items(), key=operator.itemgetter(1), reverse=True)
        return str(self.__gestures[prediction[0][0]])

    def summarize(self):
        pass
