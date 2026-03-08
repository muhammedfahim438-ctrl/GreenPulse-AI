# ══════════════════════════════
# GreenPulse AI — Flask App
# With Database + Login System
# ══════════════════════════════

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

from models import db, Farmer
from routes.predict import predict_bp
from routes.weather import weather_bp
from routes.disease import disease_bp
from routes.auth    import auth_bp

app = Flask(__name__)

# ── configuration ──
app.config['SECRET_KEY']           = 'greenpulse-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///greenpulse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ── initialize extensions ──
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
db.init_app(app)

bcrypt       = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Farmer.query.get(int(user_id))

# ── register blueprints ──
app.register_blueprint(predict_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(disease_bp)
app.register_blueprint(auth_bp)

# ── home route ──
@app.route('/')
def home():
    return {
        'message': 'GreenPulse AI Backend is Running!',
        'status':  'success',
        'version': '2.0.0'
    }

# ── create database tables ──
with app.app_context():
    db.create_all()
    print('✅ Database tables created!')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
