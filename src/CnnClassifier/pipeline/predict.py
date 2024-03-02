import numpy as np 
import tensorflow as tf 
from keras import models
from keras.models import load_model
from keras.preprocessing import image
import os


class PredictionPipeline:
    def __init__(self):
        self.model = load_model(os.path.join("artifacts", "training", "model.h5"))

    def predict(self, filepath):
        # Prepare image
        test_image = image.load_img(filepath, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        
        # Normalize if needed
        test_image = test_image / 255.0  # Add this line if your model was trained with normalized images
        
        # Predict
        result = np.argmax(self.model.predict(test_image), axis=1)

        # Match prediction to class
        if result[0] == 0:
            prediction = 'Potato___Early_blight'
        elif result[0] == 1:
            prediction = 'Potato___Late_blight'
        else:
            prediction = 'Potato___healthy'

        return [{"image": prediction}]
