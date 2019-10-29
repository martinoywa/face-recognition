import cv2
from random import randint
import pickle


face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")
cap = cv2.VideoCapture(0)

labels = {}
with open("labels.pt", "rb") as f:
	labels = pickle.load(f)
	labels = {v: k for k, v in labels.items()}

while True:
	ret, frame = cap.read()	# capture frame-by-frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
	for (x, y, w, h) in faces:
		#print(x, y, w, h)
		# Region Of Interest
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]

		# recognizer
		id_, conf = recognizer.predict(roi_gray)
		if conf >= 45:
			print(labels[id_])
			# show label on the image
			font = cv2.FONT_HERSHEY_SIMPLEX
			name = labels[id_]
			color = (255, 255, 255)
			stroke = 2
			cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

		# draw a rectangle
		color = (0, 255, 0) #BGR
		stroke = 2
		end_cord_x = x + w
		end_cord_y = y + h
		cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

	cv2.imshow('frame', frame)	# display resulting frame
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

# release when done
cap.release()
cv2.destroyAllWindows()  