# ══════════════════════════════
# GreenPulse AI — Database Models
# ══════════════════════════════

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Farmer(db.Model, UserMixin):
    __tablename__ = 'farmers'

    id           = db.Column(db.Integer, primary_key=True)
    first_name   = db.Column(db.String(50), nullable=False)
    last_name    = db.Column(db.String(50), nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    phone        = db.Column(db.String(20))
    location     = db.Column(db.String(100))
    farm_size    = db.Column(db.Float)
    primary_crop = db.Column(db.String(50))
    password     = db.Column(db.String(200), nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship to predictions
    predictions  = db.relationship('Prediction', backref='farmer', lazy=True)

    def __repr__(self):
        return f'<Farmer {self.email}>'


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id              = db.Column(db.Integer, primary_key=True)
    farmer_id       = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    crop            = db.Column(db.String(50))
    predicted_yield = db.Column(db.Float)
    total_yield     = db.Column(db.Float)
    area            = db.Column(db.Float)
    temperature     = db.Column(db.Float)
    rainfall        = db.Column(db.Float)
    humidity        = db.Column(db.Float)
    soil            = db.Column(db.String(50))
    season          = db.Column(db.String(50))
    yield_status    = db.Column(db.String(20))
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Prediction {self.crop} {self.predicted_yield}>'


class DiseaseDetection(db.Model):
    __tablename__ = 'disease_detections'

    id           = db.Column(db.Integer, primary_key=True)
    farmer_id    = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    disease      = db.Column(db.String(100))
    confidence   = db.Column(db.Float)
    severity     = db.Column(db.String(20))
    image_name   = db.Column(db.String(200))
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Disease {self.disease}>'