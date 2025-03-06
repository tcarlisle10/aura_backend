from flask import request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_bp
from app.models import db, Users, LeaderboardComment, LeaderboardLike, Friends
from app.blueprints.users.schemas import user_schema, users_schema, login_schema, comment_schema, like_schema
import os
from datetime import datetime

# Define the allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload user profile image
@users_bp.route('/<int:user_id>/upload_image', methods=['POST'])
def upload_image(user_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        # Update user profile with image path
        user = db.session.get(Users, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        user.profile_image = filename
        db.session.commit()
        
        return jsonify({"message": "Image uploaded successfully"}), 200
    return jsonify({"error": "File type not allowed"}), 400

# Get user profile image
@users_bp.route('/<int:user_id>/image', methods=['GET'])
def get_image(user_id):
    user = db.session.get(Users, user_id)
    if not user or not user.profile_image:
        return jsonify({"error": "Image not found"}), 404
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], user.profile_image)

# Delete user profile image
@users_bp.route('/<int:user_id>/delete_image', methods=['DELETE'])
def delete_image(user_id):
    user = db.session.get(Users, user_id)
    if not user or not user.profile_image:
        return jsonify({"error": "Image not found"}), 404
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user.profile_image)
    if os.path.exists(image_path):
        os.remove(image_path)
        user.profile_image = None
        db.session.commit()
        return jsonify({"message": "Image deleted successfully"}), 200
    return jsonify({"error": "Image not found"}), 404

# Get all users
@users_bp.route('/', methods=['GET'])
def get_users():
    try:
        users = db.session.scalars(db.select(Users)).all()
        return jsonify(users_schema.dump(users)), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)})

# Get a single user
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db.session.get(Users, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500

# Create a new user
@users_bp.route('/create', methods=['POST'])
def create_user():
    try:
        data = request.json

        # Validate input
        errors = user_schema.validate(data)
        if errors:
            return jsonify({"error": "Validation error", "Details": errors}), 400
        
        # Hash the password before storing
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

# Update user details
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
            user.password = generate_password_hash(data["password"]) # Hash new password

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

# User login
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

# Add comment to an image
@users_bp.route('/<int:image_id>/comment', methods=['POST'])
def add_comment(image_id):
    try:
        data = request.json
        errors = comment_schema.validate(data)
        if errors:
            return jsonify({"error": "Validation error", "details": errors}), 400
        
        new_comment = LeaderboardComment(
            leaderboard_image_id=image_id,
            user_id=data["user_id"],
            text=data["content"]
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"message": "Comment added successfully", "comment": comment_schema.dump(new_comment)}), 201
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500

# Like an image
@users_bp.route('/<int:image_id>/like', methods=['POST'])
def like_image(image_id):
    try:
        data = request.json
        errors = like_schema.validate(data)
        if errors:
            return jsonify({"error": "Validation error", "details": errors}), 400
        
        new_like = LeaderboardLike(
            leaderboard_image_id=image_id,
            user_id=data["user_id"]
        )
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"message": "Image liked successfully", "like": like_schema.dump(new_like)}), 201
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500

# Unlike an image
@users_bp.route('/<int:image_id>/unlike', methods=['DELETE'])
def unlike_image(image_id):
    try:
        data = request.json
        like = db.session.query(LeaderboardLike).filter_by(leaderboard_image_id=image_id, user_id=data["user_id"]).first()
        if not like:
            return jsonify({"error": "Like not found"}), 404
        
        db.session.delete(like)
        db.session.commit()
        return jsonify({"message": "Image unliked successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500

# Add a friend
@users_bp.route('/<int:user_id>/add_friend', methods=['POST'])
def add_friend(user_id):
    try:
        data = request.json
        new_friend = Friends(
            user_id=user_id,
            friend_id=data["friend_id"]
        )
        db.session.add(new_friend)
        db.session.commit()
        return jsonify({"message": "Friend added successfully"}), 201
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500

# Delete a friend
@users_bp.route('/<int:user_id>/delete_friend', methods=['DELETE'])
def delete_friend(user_id):
    try:
        data = request.json
        friend = db.session.query(Friends).filter_by(user_id=user_id, friend_id=data["friend_id"]).first()
        if not friend:
            return jsonify({"error": "Friend not found"}), 404
        
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"message": "Friend deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong", "message": str(e)}), 500