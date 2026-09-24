import os
import cv2
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def create_employee_folder(employee_id):
    folder_path = os.path.join("dataset", employee_id)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

employee_id = "0010"
folder_path = create_employee_folder(employee_id)

count = 0

camera = cv2.VideoCapture(0)

while count < 20:
    success, frame = camera.read()
    if not success:
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        face = frame[y:y+h, x:x+w]
        count += 1
       
        filename = os.path.join(folder_path, f"face_{count}.jpg")
        cv2.imwrite(filename, face)
    
    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()


