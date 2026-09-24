import cv2
import sqlite3
from database import record_attendance

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

connection = sqlite3.connect("attendance.db")
cursor = connection.cursor()

recognized_employee = None

while True:

    success, frame = camera.read()

    if not success:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray)

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        print(label, confidence)

        name = "Unknown"

        if confidence < 70:

            cursor.execute(
                """
                SELECT employee_id, name, department
                FROM employees
                WHERE employee_id = ?
                """,
                (str(label).zfill(4),)
            )

            employee = cursor.fetchone()

            if employee:

                name = employee[1]

                recognized_employee = employee

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 0),
            2
        )

    cv2.imshow("Face Recognition", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        if recognized_employee:

            record_attendance(recognized_employee[0])

            print(
                f"Attendance recorded for {recognized_employee[1]}"
            )

        else:

            print(
                "No recognized employee. Attendance not recorded."
            )

        break


camera.release()
cv2.destroyAllWindows()
connection.close()