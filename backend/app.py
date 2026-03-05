# ══════════════════════════════
# GreenPulse AI — Main Flask App
# ══════════════════════════════

from flask import Flask
from flask_cors import CORS
from routes.predict import predict_bp
from routes.weather import weather_bp
from routes.disease import disease_bp

# create Flask app
app = Flask(__name__)

# allow frontend to talk to backend
CORS(app)

# ── register all routes ──
app.register_blueprint(predict_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(disease_bp)

# ── home route to test server ──
@app.route('/')
def home():
    return {
        'message': 'GreenPulse AI Backend is Running!',
        'status':  'success',
        'version': '1.0.0'
    }

# ── start the server ──
if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )