
from detection.Detectface import DetectFaceClass
from frontalization.frontalization import *
import cv2

import openface
import numpy as np
import pandas as pd

from operator import itemgetter
from sklearn.pipeline import Pipeline
from sklearn.lda import LDA
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.mixture import GMM
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

import pdb

PATH = '/home/oleg/recognition/faces/Arnold-Schwarzenegger-Family-Pictures-Wife-Son-Daughter-Age.jpg'


class FaceRecognition(object):
	def __init__(self, threshold, detection_net):
		
		self.threshold = threshold
		fileDir = os.path.dirname(os.path.realpath(__file__))
		recognitionModelDir = os.path.join(fileDir, 'recognition', 'models', 'openface', 'nn4.small2.v1.t7')
		
		self.detectionNN = detection_net
		
		self.frontalization = Frontalization()
		self.recognitionNN = openface.TorchNeuralNet(recognitionModelDir, imgDim=96, cuda=True)

		self.labelsPath = os.path.join(fileDir, 'data','labels.csv')
		self.labels = pd.read_csv(self.labelsPath)
		self.embeddingsPath = os.path.join(fileDir, 'data','reps.csv')
		self.embeddings = np.genfromtxt(self.embeddingsPath, delimiter=",",usecols=np.arange(0,128))
		if(self.embeddings.size == 128):
			self.embeddings.shape = (1, 128)
		

	def recognize(self, img):
		#pdb.set_trace()
		boxes = self.detectionNN.detect_Face(img)
		faces = []


		for box in boxes:
			faces.append(img[box[1]:box[3], box[0]:box[2]])

		labels = []
		
		for face in faces:
			print(face.shape)
			
			smallFace = face

			resize_factor = 1

			if (smallFace.shape[0] > smallFace.shape[1]):
				resize_factor = 96. / smallFace.shape[1]
			else:
				resize_factor = 96. / smallFace.shape[0]

			smallFace = cv2.resize(smallFace, (int(smallFace.shape[1] * resize_factor), int(smallFace.shape[0] * resize_factor)))

			#cv2.imshow("Image", smallFace)
			#cv2.waitKey(0)

			Frontalized = self.frontalization.frontalize(smallFace)

			cv2.imwrite("/home/oleg/server_assembly/recognition/Image.jpg", Frontalized)
			#cv2.waitKey(0)


			cropedAlignedfaces = self.detectionNN.detect_Face(Frontalized)
			if len(cropedAlignedfaces) == 0:
				print(len(cropedAlignedfaces))
				continue
			box = cropedAlignedfaces[0]
			cropedAligned = Frontalized[box[1]:box[3], box[0]:box[2]]

			#cv2.imshow("Image", cropedAligned)
			#cv2.imwrite("/home/oleg/cropped.png", cropedAligned)
			#cv2.waitKey(0)

			face96 = cv2.resize(cropedAligned, (96, 96))
			#cv2.imshow("Image", face96)
			#cv2.waitKey(0)

			face96RGB = cv2.cvtColor(face96.astype(np.uint8), cv2.COLOR_BGR2RGB)

			rep = self.recognitionNN.forward(face96RGB)
			labels.append(self.match(rep))
		

		return labels

	def match(self, frep):
		best = 10
		best_i = 0;
		for i, rep in enumerate(self.embeddings):
			val = np.linalg.norm(rep - frep)
			if val < best:
				best = val
				best_i = i

		print("Distance: " + str(best))
		if best > self.threshold:
			return "I don't know :("

		return self.labels['name'][best_i]


	def add(self, img, name, img_name):
		faces = self.detectionNN.detect_Face(img)
		if (len(faces) > 1):
			return "too many people! must be 1!"

		if (len(faces) < 1):
			return "I don't see any one here :("
		
		box = faces[0]
		face = img[box[1]:box[3], box[0]:box[2]]
		smallFace = face

		resize_factor = 1

		if (smallFace.shape[0] > smallFace.shape[1]):
			resize_factor = 96. / smallFace.shape[1]
		else:
			resize_factor = 96. / smallFace.shape[0]

		smallFace = cv2.resize(smallFace, (int(smallFace.shape[1] * resize_factor), int(smallFace.shape[0] * resize_factor)))

		Frontalized = self.frontalization.frontalize(smallFace)
		cropedAlignedBox = self.detectionNN.detect_Face(Frontalized)[0]

		cropedAligned = Frontalized[cropedAlignedBox[1]:cropedAlignedBox[3], cropedAlignedBox[0]:cropedAlignedBox[2]]

		face96 = cv2.resize(cropedAligned, (96, 96))
		#cv2.imshow("Image", face96)
		#cv2.waitKey(0)

		face96RGB = cv2.cvtColor(face96, cv2.COLOR_BGR2RGB)

		rep = self.recognitionNN.forward(face96RGB)

		fileName = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'pitures', img_name)
		cv2.imwrite(fileName, cropedAligned)

		tmp = pd.DataFrame([[fileName, name]], columns=['picture', 'name'])
		print("labels before")
		print(self.labels)
		print("new label")
		print(tmp)
		if self.labels.empty:
			print("label was empty - overwriting")
			self.labels = tmp
		else:
			print("appending labels")
			#self.labels.append(tmp, ignore_index=True)
			self.labels = pd.concat([self.labels, tmp], ignore_index=True)
		print("new labels")
		print(self.labels)

		rep.shape = (1, rep.size)
		print("embeddings before")
		print(self.embeddings)
		print(self.embeddings.shape)
		print("new embeddings")
		print(rep)
		if self.embeddings.size == 0:
			print("embeddings were empty - overwriting")
			self.embeddings = rep
		else:
			print("appending embeddings")
			self.embeddings = np.append(self.embeddings, rep, axis=0)

		print("new")
		print(self.embeddings)
		print(self.labels)
		# save values
		self.labels.to_csv(self.labelsPath, columns=["picture", 'name'], index=False)
		np.savetxt(self.embeddingsPath, self.embeddings, delimiter=",")

		return "success"




		

if __name__ == "__main__":
	faceRecognizer = FaceRecognition(1.1)
	Image = cv2.imread(PATH)
	labels = faceRecognizer.recognize(Image)
	print(labels)
