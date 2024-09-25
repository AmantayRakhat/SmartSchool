from flask import Flask, jsonify, request, send_from_directory, render_template
import firebase_admin
from flask_cors import CORS
import time
from firebase_admin import credentials, db

from flask import Flask, render_template, Response, request, jsonify, send_from_directory
import cv2
import os
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app)


# Инициализация Firebase
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://safetyschool-19925-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# cred = credentials.RefreshToken('key.json')
# default_app = firebase_admin.initialize_app(cred)

# Пример функции для чтения данных из Firebase
def read_data():
    ref = db.reference('/')
    data = ref.get()
    return data

@app.route('/data')
def index():
    return read_data()

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

@app.route('/esp1/status', methods=['GET'])
def get_esp1_status():
    ref = db.reference('/esp1')  # Путь к данным esp1 в Firebase
    data = ref.get()
    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify({"error": "Data not found"}), 404

@app.route('/toggle-terrorism', methods=['POST'])
def toggle_terrorism():
    terrorism_data = request.json
    status1 = terrorism_data['status1']  # Получаем новое состояние (0 или 1)
    status2 = terrorism_data['status2']
    # Обновляем состояние дверей door и door1
    ref_door = db.reference('esp1/door')
    ref_door.set(status1)

    ref_door1 = db.reference('esp1/door1')
    ref_door1.set(status1)

    ref_red = db.reference('esp1/red')
    ref_red.set(status2)

    ref_red1 = db.reference('esp1/red1')
    ref_red1.set(status2)

    return jsonify({"success": True, "door_status": status1, "red": status2}), 200

@app.route('/esp2/data', methods=['GET'])
def get_esp2_data():
    ref = db.reference('/esp2')
    data = ref.get()
    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify({"error": "Data not found"}), 404

# @app.route('/play-school-bell', methods=['POST'])
# def play_school_bell():
#     # Обновляем данные в esp2 для воспроизведения звонка
#     ref = db.reference('/esp2')
#     ref.update({
#         'select': 1,    # Значение 2 соответствует файлу 001.mp3
#         'playStop': 0   # 0 для воспроизведения
#     })
#     return jsonify({"success": True}), 200

@app.route('/play-bell', methods=['POST'])
def play_bell():
    data = request.json
    play = data.get('play')

    if play:
        # Установить первый аудиофайл (например, звонок) и запустить воспроизведение
        ref_select = db.reference('/esp2/select')
        ref_select.set(1)  # Устанавливаем первый трек (001.mp3)

        ref_playStop = db.reference('/esp2/playStop')
        ref_playStop.set(0)  # Включаем воспроизведение

        return jsonify({"success": True, "message": "Школьный звонок включен"}), 200

    return jsonify({"success": False, "message": "Не удалось включить звонок"}), 400

# Добавляем новый маршрут для управления состоянием "Ескерту жүйесі"
@app.route('/toggle-alarm', methods=['POST'])
def toggle_alarm():
    alarm_data = request.json
    status = alarm_data['status']  # Получаем новое состояние (0 или 1)

    # Обновляем состояние 'alarm' в Firebase
    ref_alarm = db.reference('esp2/alarm')
    ref_alarm.set(status)

    return jsonify({"success": True, "alarm_status": status}), 200


# Получение данных об освещении
@app.route('/light-status', methods=['GET'])
def get_light_status():
    ref = db.reference('/esp3')  # Путь к данным об освещении
    light_status = ref.get()
    return jsonify(light_status), 200

# Изменение состояния освещения
@app.route('/toggle-light', methods=['POST'])
def toggle_light():
    light_data = request.json
    light_name = light_data['name']  # Название света, например 'zharyq1'
    light_status = light_data['status']  # Новое состояние света, например 0 или 1
    
    ref = db.reference(f'/esp3/{light_name}')
    ref.set(light_status)
    return jsonify({"success": True}), 200

@app.route('/esp4/status', methods=['GET'])
def get_esp4_status():
    ref = db.reference('/esp4/cab1')
    status = ref.get()
    if status is not None:
        return jsonify(status), 200
    else:
        return jsonify({"error": "Data not found"}), 404

@app.route('/esp4/set-temperature', methods=['POST'])
def set_esp4_temperature():
    # Предполагается, что JSON тело запроса будет содержать 'maxtemp' и 'mintemp'
    data = request.json
    max_temp = int(data.get('maxtemp'))
    min_temp = int(data.get('mintemp'))

    if max_temp is not None and min_temp is not None:
        ref = db.reference('/esp4/cab1')
        ref.update({"maxtemp": max_temp, "mintemp": min_temp})
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

# @app.route('/esp5/data', methods=['GET'])
# def get_esp5_data():
#     ref = db.reference('/esp5')
#     data = ref.get()
#     if data is not None:
#         # Возвращает данные в формате JSON
#         return jsonify(data), 200
#     else:
#         # Если данных нет, возвращает ошибку
#         return jsonify({"error": "Data not found"}), 404
    
# @app.route('/light-statusDala', methods=['GET'])
# def get_light_statusD():
#     ref = db.reference('/esp6')  # Путь к данным об освещении
#     light_status = ref.get()
#     return jsonify(light_status), 200

# Изменение состояния освещения
# @app.route('/toggle-lightDala', methods=['POST'])
# def toggle_lightD():
#     light_data = request.json
#     light_name = light_data['name']  # Название света, например 'zharyq1'
#     light_status = light_data['status']  # Новое состояние света, например 0 или 1
    
#     ref = db.reference(f'/esp6/{light_name}')
#     ref.set(light_status)
#     return jsonify({"success": True}), 200

@app.route('/esp7/data', methods=['GET'])
def get_esp7_data():
    ref = db.reference('/esp7')
    data = ref.get()
    if data is not None:
        # Возвращает данные в формате JSON
        return jsonify(data), 200
    else:
        # Если данных нет, возвращает ошибку
        return jsonify({"error": "Data not found"}), 404

@app.route('/esp7/set-humidity', methods=['POST'])
def set_esp7_humidity():
    # Предполагается, что JSON тело запроса будет содержать 'maxtemp' и 'mintemp'
    data = request.json
    max_hum = int(data.get('maxhum'))
    min_hum = int(data.get('minhum'))

    if max_hum is not None and min_hum is not None:
        ref = db.reference('/esp7')
        ref.update({"maxvlazh": max_hum, "minvlazh": min_hum})
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400
    
@app.route('/opencv')
def about1():
    return render_template('opencv.html')

@app.route('/earthquake')
def about2():
    return send_from_directory('static', 'earthquake.html')

camera = cv2.VideoCapture(0)  # Используйте 0 для основной камеры

# Загрузка предварительно обученной модели Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def generate_frames():
    while True:
        success, frame = camera.read()  # Читаем кадр
        if not success:
            break
        else:
            faces = face_cascade.detectMultiScale(frame, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def face_recognition(frame):
    # Предполагается, что в 'face_images/' хранятся изображения для сверки
    faces_detected = face_cascade.detectMultiScale(frame, 1.1, 4)
    for (x, y, w, h) in faces_detected:
        roi_color = frame[y:y+h, x:x+w]
        files = os.listdir('face_images/')
        for file in files:
            face_image = cv2.imread(f'face_images/{file}')
            try:
                # Сравнение с использованием гистограмм
                hist1 = cv2.calcHist([roi_color], [0], None, [256], [0,256])
                hist2 = cv2.calcHist([face_image], [0], None, [256], [0,256])
                result = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                if result > 0.6:  # Порог сходства
                    return f"Лицо идентифицировано как {file.split('.')[0]}"
            except Exception as e:
                print(e)
        return "Лицо не идентифицировано"
    return "Лицо не обнаружено"

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/verify', methods=['POST'])
def verify():
    success, frame = camera.read()
    if not success:
        return jsonify({'error': 'Ошибка захвата изображения'}), 500

    result = face_recognition(frame)
    if "Лицо идентифицировано как" in result:
        # Если лицо успешно идентифицировано, устанавливаем esp1/door в 1
        ref = db.reference('esp1/door')
        ref.set(1)

        # Задержка на 4 секунды перед установкой значения обратно в 0
        time.sleep(4)
        ref.set(0)

        return result
    else:
        return result


@app.route('/capture_face', methods=['POST'])
def capture_face():
    success, frame = camera.read()
    if not success:
        return jsonify({'error': 'Не удалось захватить изображение.'}), 500

    faces = face_cascade.detectMultiScale(frame, 1.1, 4)
    if len(faces) == 0:
        return jsonify({'error': 'Лица не обнаружены.'}), 400

    # Получаем имя из данных запроса
    face_name = request.form.get('faceName', 'Unknown')  # Используем 'Unknown' как значение по умолчанию

    save_path = 'face_images'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Сохраняем каждое обнаруженное лицо с использованием предоставленного имени
    for i, (x, y, w, h) in enumerate(faces):
        face_img = frame[y:y+h, x:x+w]
        file_name = f"{face_name}.jpg"  # Имя файла формируется из имени, предоставленного пользователем, и индекса лица
        cv2.imwrite(os.path.join(save_path, file_name), face_img)

    return jsonify({'message': f'Лица успешно сохранены под именем {face_name}.'}), 200

@app.route('/get_faces')
def get_faces():
    faces = []
    for filename in os.listdir('face_images'):
        faces.append(filename)
    return jsonify(faces)


# Предполагая, что 'face_images' находится в корне проекта
@app.route('/faces/<filename>')
def send_face(filename):
    return send_from_directory('face_images', filename)


if __name__ == '__main__':
    app.run(debug=True)

