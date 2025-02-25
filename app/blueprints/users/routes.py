from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_bp
from app.models import db, Users
from datetime import datetime
from app.blueprints.users.schema import user_schema, users_schema, login_schema


# get all users
@users_bp.route('/', methods=['GET'])
def get_users():
    try:
        users = db.session.scalars(db.select(Users)).all()
        return jsonify(users_schema.dump(users)), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)})
    
# get a single user
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db.session.get(Users, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500
    
# create a new user
@users_bp.route('/create', methods=['Post'])
def create_user():
    try:
        data = request.json

        # validate input
        errors = user_schema.validate(data)
        if errors:
            return jsonify({"error": "Validation error", "Details": errors}), 400
        
        # hash the password before storing
        hashed_password = generate_password_hash(data["password"])

        dob = None
        if "dob" in data and data["dob"]:
            dob = datetime.strptime(data["dob"], "%Y-%m-%d").date() 

        new_user = Users(
            name=data["name"],
            email=data["email"],
            phone=data.get("phone"),
            dob=dob,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
    
        return jsonify({"message": "User created successfully", "id": new_user.id}), 201
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500
    
# updating user
@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = db.session.get(Users, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.json
        errors = user_schema.validate(data, partial=True)
        if errors:
            return jsonify({"error": "Validation error", "detail": errors}), 400
        
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        user.phone = data.get("phone", user.phone)
        

        if "dob" in data and data["dob"]:
            try:
                user.dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()  # Convert string to date
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        if "password" in data:
            user.password = generate_password_hash(data["password"]) # hash new password

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500
    
# Delete user
@users_bp.route('/delete/<int:user_id>', methods=['DELETE'])  
def delete_user(user_id):
    try:
        
        user = db.session.get(Users, user_id)
        if not user:
            return jsonify({"error": "User does not exist"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User successfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500
    
# login
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        errors = login_schema.validate(data)
        if errors:
            return jsonify({"error": "Validation error", "details": errors}), 400
        
        
        stmt = db.select(Users).where(Users.email == data["email"])
        user = db.session.execute(stmt).scalar_one_or_none()

        if not user or not check_password_hash(user.password, data["password"]):
            return jsonify({"error": "Invalid email or password"}), 401

        return jsonify({"message": "Login Successful", "user_id": user.id}), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500