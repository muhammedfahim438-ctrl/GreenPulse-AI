# ══════════════════════════════
# GreenPulse AI — Auth Routes
# Login, Register, Logout
# ══════════════════════════════

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Farmer
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt  = Bcrypt()


# ── Register new farmer ──
@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    # check if email already exists
    existing = Farmer.query.filter_by(
        email=data.get('email')
    ).first()

    if existing:
        return jsonify({
            'status':  'error',
            'message': 'Email already registered!'
        }), 400

    # hash password
    hashed_pw = bcrypt.generate_password_hash(
        data.get('password')
    ).decode('utf-8')

    # create new farmer
    farmer = Farmer(
        first_name   = data.get('first_name'),
        last_name    = data.get('last_name'),
        email        = data.get('email'),
        phone        = data.get('phone', ''),
        location     = data.get('location', ''),
        farm_size    = data.get('farm_size', 0),
        primary_crop = data.get('primary_crop', ''),
        password     = hashed_pw
    )

    db.session.add(farmer)
    db.session.commit()

    return jsonify({
        'status':  'success',
        'message': 'Registration successful!',
        'farmer':  {
            'id':         farmer.id,
            'first_name': farmer.first_name,
            'last_name':  farmer.last_name,
            'email':      farmer.email
        }
    })


# ── Login farmer ──
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data     = request.get_json()
    email    = data.get('email')
    password = data.get('password')

    # find farmer by email
    farmer = Farmer.query.filter_by(email=email).first()

    if not farmer:
        return jsonify({
            'status':  'error',
            'message': 'Email not found!'
        }), 401

    # check password
    if not bcrypt.check_password_hash(farmer.password, password):
        return jsonify({
            'status':  'error',
            'message': 'Wrong password!'
        }), 401

    # login the farmer
    login_user(farmer)

    return jsonify({
        'status':  'success',
        'message': 'Login successful!',
        'farmer':  {
            'id':         farmer.id,
            'first_name': farmer.first_name,
            'last_name':  farmer.last_name,
            'email':      farmer.email,
            'location':   farmer.location,
            'primary_crop': farmer.primary_crop
        }
    })


# ── Logout farmer ──
@auth_bp.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({
        'status':  'success',
        'message': 'Logged out successfully!'
    })


# ── Get current farmer profile ──
@auth_bp.route('/api/auth/profile', methods=['GET'])
@login_required
def profile():
    farmer = current_user
    return jsonify({
        'status': 'success',
        'farmer': {
            'id':           farmer.id,
            'first_name':   farmer.first_name,
            'last_name':    farmer.last_name,
            'email':        farmer.email,
            'phone':        farmer.phone,
            'location':     farmer.location,
            'farm_size':    farmer.farm_size,
            'primary_crop': farmer.primary_crop,
            'created_at':   str(farmer.created_at)
        }
    })