from flask import Flask, jsonify, request, send_from_directory, render_template
import firebase_admin
from flask_cors import CORS

from firebase_admin import credentials, db

app = Flask(__name__)
CORS(app)

# Инициализация Firebase
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://safetyschool-5bb16-default-rtdb.asia-southeast1.firebasedatabase.app'
})
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

@app.route('/esp5/data', methods=['GET'])
def get_esp5_data():
    ref = db.reference('/esp5')
    data = ref.get()
    if data is not None:
        # Возвращает данные в формате JSON
        return jsonify(data), 200
    else:
        # Если данных нет, возвращает ошибку
        return jsonify({"error": "Data not found"}), 404
    
@app.route('/light-statusDala', methods=['GET'])
def get_light_statusD():
    ref = db.reference('/esp6')  # Путь к данным об освещении
    light_status = ref.get()
    return jsonify(light_status), 200

# Изменение состояния освещения
@app.route('/toggle-lightDala', methods=['POST'])
def toggle_lightD():
    light_data = request.json
    light_name = light_data['name']  # Название света, например 'zharyq1'
    light_status = light_data['status']  # Новое состояние света, например 0 или 1
    
    ref = db.reference(f'/esp6/{light_name}')
    ref.set(light_status)
    return jsonify({"success": True}), 200

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
    return send_from_directory('static', 'opencv.html')

@app.route('/earthquake')
def about2():
    return send_from_directory('static', 'earthquake.html')


if __name__ == '__main__':
    app.run(debug=True)

