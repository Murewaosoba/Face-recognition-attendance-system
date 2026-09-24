import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

dataset_path = "dataset"

for employee_id in os.listdir(dataset_path):
    employee_folder = os.path.join(dataset_path, employee_id)

    for image_name in os.listdir(employee_folder):
        image_path = os.path.join(employee_folder, image_name)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        faces.append(image)
        labels.append(int(employee_id))

recognizer.train(faces, np.array(labels))

recognizer.write("face_model.yml")