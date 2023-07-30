import os
import datetime
import cv2
from flask import Flask, request, jsonify, render_template
import face_recognition

app = Flask(__name__)

# Simpan data pendaftaran dalam variabel sementara (ini hanya contoh, biasanya data disimpan dalam database)
registered_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    photo = request.files['photo']

    # Simpan foto di folder uploads
    uploads_folder = os.path.join(os.getcwd(), 'static', 'uploads')
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
    photo.save(os.path.join(uploads_folder, f'{datetime.date.today()}_{name}.jpg'))

    # Simpan data pendaftaran (hanya contoh, biasanya data disimpan dalam database)
    registered_data[name] = f'{datetime.date.today()}_{name}.jpg'

    response = {'success': True, 'name': name}
    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    photo = request.files['photo']

    # Simpan foto login di folder uploads
    uploads_folder = os.path.join(os.getcwd(), 'static', 'uploads')
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
    login_filename = os.path.join(uploads_folder, 'login_face.jpg')
    photo.save(login_filename)

    # Face detection on the login photo using Haar Cascades
    login_image = cv2.imread(login_filename)
    gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)

    # Load the Haar Cascades face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        # No face detected in the login photo
        response = {'success': False}
        return jsonify(response)

    # Process face recognition for the login face
    login_image = face_recognition.load_image_file(login_filename)
    login_face_encodings = face_recognition.face_encodings(login_image)

    print("Number of face encodings in login image:", len(login_face_encodings))

    # Proses perbandingan foto login dengan foto pendaftaran menggunakan face recognition
    for name, filename in registered_data.items():
        registered_photo = os.path.join(uploads_folder, filename)
        registered_image = face_recognition.load_image_file(registered_photo)

        # Process face recognition for the registered face
        registered_face_encodings = face_recognition.face_encodings(registered_image)

        print("Number of face encodings in registered image:", len(registered_face_encodings))

        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
            # Compare the face encodings of the login face and the registered face
            matches = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])

            print("Matches:", matches)

            if any(matches):
                response = {'success': True, 'name': name}
                return jsonify(response)

    # No match found, return failure response
    response = {'success': False}
    return jsonify(response)


@app.route('/success')
def success():
    user_name = request.args.get('user_name')
    return render_template('success.html', user_name=user_name)

if __name__ == '__main__':
    app.run(debug=True)