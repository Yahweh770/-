from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from strodservice.utils.websocket_logger import log_websocket_event
from strodservice.utils.notification_sender import send_email, send_sms
from strodservice.utils.file_storage import save_file
from flask import send_from_directory
import jwt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# === Модели ===
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='employee')

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)

class FieldData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer)
    line_type = db.Column(db.String)
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    material_used = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String)

# === Функции аутентификации ===
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Токен отсутствует!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Токен недействителен!'}), 401

        return f(current_user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

def role_required(roles):
    def wrapper(f):
        @token_required
        def decorated(current_user, *args, **kwargs):
            if current_user.role not in roles:
                return jsonify({'message': 'Недостаточно прав!'}), 403
            return f(current_user, *args, **kwargs)
        decorated.__name__ = f.__name__
        return decorated
    return wrapper

# === WebSocket события ===
@socketio.on('connect')
def handle_connect():
    print('Клиент подключился')

@socketio.on('send_notification')
def handle_notification(data):
    emit('new_notification', data, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    emit('new_message', {
        'username': data['username'],
        'message': data['message'],
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    log_websocket_event(data['username'], 'message', data['message'])
    emit('new_message', {
        'username': data['username'],
        'message': data['message'],
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

@socketio.on('send_file')
def handle_file(data):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = save_file(file)
        emit('new_file', {
            'username': data['username'],
            'filename': filename,
            'url': f'/uploads/{filename}',
            'timestamp': datetime.now().isoformat()
        }, broadcast=True)

# === API ===
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password_hash=hashed_password, role=data.get('role', 'employee'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Пользователь создан!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Неверные данные!'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

@app.route('/api/objects', methods=['GET'])
@token_required
def get_objects(current_user):
    objects = Object.query.all()
    return jsonify([{'id': o.id, 'name': o.name, 'location': o.location} for o in objects])

@app.route('/api/field_data', methods=['GET'])
@token_required
def get_field_data(current_user):
    data = FieldData.query.all()
    return jsonify([{
        'id': d.id,
        'object_id': d.object_id,
        'line_type': d.line_type,
        'length': d.length,
        'width': d.width,
        'material_used': d.material_used,
        'date': d.date.isoformat(),
        'notes': d.notes
    } for d in data])

@app.route('/api/field_data', methods=['POST'])
@token_required
def add_field_data(current_user):
    data = request.json
    new_record = FieldData(
        object_id=data['object_id'],
        line_type=data['line_type'],
        length=data['length'],
        width=data['width'],
        material_used=data['material_used'],
        notes=data['notes']
    )
    db.session.add(new_record)
    db.session.commit()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

    # ✅ Отправить уведомление через WebSocket
    socketio.emit('new_notification', {
        'message': f'Новые полевые данные добавлены пользователем {current_user.username}',
        'type': 'info'
    })

    return jsonify({'status': 'success'})

@app.route('/api/users', methods=['GET'])
@role_required(['admin'])
def get_users(current_user):
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'role': u.role} for u in users])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

@app.route('/api/field_data', methods=['POST'])
@token_required
def add_field_data(current_user):
    data = request.json
    new_record = FieldData(
        object_id=data['object_id'],
        line_type=data['line_type'],
        length=data['length'],
        width=data['width'],
        material_used=data['material_used'],
        notes=data['notes']
    )
    db.session.add(new_record)
    db.session.commit()

    socketio.emit('new_notification', {
        'message': f'Новые полевые данные добавлены пользователем {current_user.username}',
        'type': 'info'
    })

    # ✅ Отправить email/SMS
    send_email('manager@company.com', 'Новые данные', 'Проверьте новые данные.')
    send_sms('+1234567890', 'Новые данные добавлены.')

    return jsonify({'status': 'success'})