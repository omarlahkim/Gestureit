from keras_squeezenet import SqueezeNet
from keras.layers import Activation, Dropout, GlobalAveragePooling2D,Convolution2D
from Gestures import Gestures


g = Gestures()
gestures = g.getGestures()

#LAYERS used in the cnn
CNN_LAYERS = [SqueezeNet(input_shape=(225, 225, 3), include_top=False),Dropout(0.5),Convolution2D(len(gestures), (1, 1), padding='valid'),Activation('relu'),GlobalAveragePooling2D(),Activation('softmax')]


