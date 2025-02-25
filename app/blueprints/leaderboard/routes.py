from flask import request, jsonify, Blueprint
from . import leaderboard_bp
from app.models import db, Leaderboard, LeaderboardLike, LeaderboardComment
from .schemas.leaderboard_schema import LeaderboardSchema
from .schemas.likes_schema import LikeSchema
from .schemas.comments_schema import CommentSchema

# Create instances of the schemas
leaderboard_schema = LeaderboardSchema()
like_schema = LikeSchema()
comment_schema = CommentSchema()

# Get all leaderboard images
@leaderboard_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        # get all leaderboard images
        leaderboard = Leaderboard.queary.all()
        # return the leaderboard images
        return jsonify(leaderboard_schema.dump(leaderboard, many=True)), 200
    # except statement to catch any exceptions that may occur
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Add a new leaderboard image
@leaderboard_bp.route('/add_image', methods=['POST'])
def add_leaderboard():
    try:
        # get the data from the request
        data = request.get.json()
        # validate the data
        errors = leaderboard_schema.validate(data)
        # if there are errors, return a 400 response
        if errors:
            return jsonify({'error': 'Validation errors', 'details': errors}), 400
        # create a new leaderboard image object
        new_entry = Leaderboard(
            image_path = data['image_path'],
            user_id = data['user_id'],
            original_image_id = data['original_image_id']
        )
        # add the new entry to the database
        db.session.add(new_entry)
        db.session.commit()

        # return the newly created leaderboard image
        return jsonify(leaderboard_schema.dump(new_entry)), 201
    # except statement to catch any exceptions that may occur
    except Exception as e:
        # return a server error message if an exception occurs
        return jsonify({'error': 'Something went wrong', 'message': str(e)}), 500
    
# Add a like to a leaderboard image
@leaderboard_bp.route('/<int:image_id>/like', methods=['POST'])
def like_leaderboard(image_id):
    try:
        # get the leaderboard image by id
        data = request.get.json()
        # validate the data
        errors = like_schema.validate(data)
        # if there are errors, return a 400 response
        if errors:
            return jsonify({'error': 'Validation errors', 'details': errors}), 400
        
        # create a new like object
        new_like = LeaderboardLike(user_id=data['user_id'], leaderboard_image_id=image_id)

        # add the like to the database
        db.session.add(new_like)
        # commit the changes
        db.session.commit()
        # return a success message
        return jsonify(like_schema.dump(new_like)), 201
    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'message': str(e)}), 500
    
# Add a comment to a leaderboard image
@leaderboard_bp.route('/<int:image_id>/comment', methods=['POST'])
def comment_leaderboard(image_id):
    try:
        # get the leaderboard image by id
        data = request.get.json()
        # validate the data 
        errors = comment_schema.validate(data)
        # if there are errors, return a 400 response
        if errors:
            return jsonify({'error': 'Validation errors', 'details': errors}), 400
        
        # create a new comment object
        new_comment = LeaderboardComment(
            text = data['text'],
            user_id = data['user_id'],
            leaderboard_image_id = image_id

        )
        # add the comment to the database
        db.session.add(new_comment)
        # commit the changes
        db.session.commit()
        # return a success message
        return jsonify(comment_schema.dump(new_comment)), 201
    # except statement to catch any exceptions that may occur
    except Exception as e:
        # return a server error message if an exception occurs
        return jsonify({'error': 'Something went wrong', 'message': str(e)}), 500
    