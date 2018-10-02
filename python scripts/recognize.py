import os
import numpy as np
import pickle
from PIL import Image
import cv2
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load prebuilt model for Frontal Face
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.createLBPHFaceRecognizer()
image_dir = os.path.join(BASE_DIR, "images")

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root,file)
            label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
            #print(label,path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            #print(label_ids)

            y_labels.append(label) #some number
            x_train.append(path) #verify this image, turn into numpy array, Gray
            pil_image = Image.open(path).convert("L")
            image_array = np.array(pil_image, "uint8")
            #print(image_array)
            faces = faceCascade.detectMultiScale(np.array(image_array), scaleFactor = 1.5, minNeighbors = 5)
            for (x,y,w,h) in faces:
                roi = image_array[ y : y + h , x : x + w ]
                x_train.append(roi)
                y_labels.append(id_)

with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids,f)


recognizer.train(x_train, np.array(y_labels))
recognizer.save("reainer.yml")
