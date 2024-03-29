import os
from PIL import Image
import numpy as np
import cv2
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# label ids
current_id = 0
label_ids = {}

# data set
x_train = []
y_labels = [] 

for root, dirs, files in os.walk(IMAGE_DIR):
	for file in files:
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root, file)
			# label = os.path.basename(os.path.dirname(path)).replace(" ", "_").lower()
			label = os.path.basename(root).replace(" ", "_").lower()
			# generating labels
			if label not in label_ids:
				label_ids[label] = current_id
				current_id += 1

			id_ = label_ids[label]
			# cread image using pillow and convert to numpy array 
			pil_image = Image.open(path).convert('L')
			image_array = np.array(pil_image, "uint8")

			# detecting faces
			faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

			for (x, y, w, h) in faces:
				roi = image_array[y:y+h, x:x+w]
				# generating training data
				x_train.append(roi)
				y_labels.append(id_)


with open("labels.pt", "wb") as f:
	pickle.dump(label_ids, f)


recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")