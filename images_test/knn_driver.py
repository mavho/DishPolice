import face_recognition
import cv2
import numpy as np
import time
import os

import knn

def get_images():
    images = []
    for image_file in os.listdir('.'):
        if image_file.endswith(".png"):
            images.append(image_file)
            
    return images

if __name__ == "__main__":
    print(get_images())
    for image in get_images():
        predictions = knn.predict(image, model_path="trained_knn_model.clf")
    
    for name, (top, right, bottom, left) in predictions:
        print("- Found {} at ({}, {})".format(name, left, top))
        
    knn.show_prediction_labels_on_image(image, predictions)