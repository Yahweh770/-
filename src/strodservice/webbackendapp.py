from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_swagger_ui import get_swaggerui_blueprint
import jwt
import os
import uuid
from werkzeug.utils import secure_filename
from utils.erp_integration import ERPIntegration
from core.excel_reports import generate_excel_report

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Executive Doc API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

ERP_CONFIG = {
    'base_url': 'https://your-1c-server.com/api',
    'username': 'your_username',
    'password': 'your_password'
}

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

@socketio.on('send_message')
def handle_message(data):
    emit('new_message', {
        'username': data['username'],
        'message': data['message'],
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@socketio.on('send_file')
def handle_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1]
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        emit('new_file', {
            'username': request.form['username'],
            'filename': unique_filename,
            'url': f'/uploads/{unique_filename}',
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

    socketio.emit('new_notification', {
        'message': f'Новые полевые данные добавлены пользователем {current_user.username}',
        'type': 'info'
    })

    return jsonify({'status': 'success'})

@app.route('/api/sync_to_erp', methods=['POST'])
@role_required(['admin'])
def sync_to_erp(current_user):
    from database.models import Object, Material
    session = Session()
    objects = session.query(Object).all()
    materials = session.query(Material).all()
    session.close()

    erp.sync_objects_to_erp(objects)
    erp.sync_materials_to_erp(materials)

    return jsonify({'status': 'success', 'message': 'Синхронизация с ERP завершена'})

@app.route('/api/export_excel', methods=['GET'])
@token_required
def export_excel(current_user):
    filepath = f"reports/field_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    generate_excel_report(filepath)
    return send_file(filepath, as_attachment=True)

@app.route('/api/users', methods=['GET'])
@role_required(['admin'])
def get_users(current_user):
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'role': u.role} for u in users])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)