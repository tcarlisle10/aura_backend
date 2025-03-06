from app.extensions import ma
from app.models import Leaderboard, LeaderboardLike, LeaderboardComment


class LeaderboardSchema(ma.SQLAlchemyAutoSchema): # ma is marshmallow || SQLAlchemyAutoSchema is a class that generates a schema from a SQLAlchemy model
    class Meta:
        # model is the model || Leaderboard is the model
        model = Leaderboard
        include_fk = True

    # Dynamic fields for like and comment counts
    like_count = ma.Method("get_like_count") # ma is marshmallow || Method is a field that allows you to define a method that will be called to get the value of the field
    comment_count = ma.Method("get_comment_count") # ma is marshmallow || Method is a field that allows you to define a method that will be called to get the value of the field

    def get_like_count(self, obj):
        """Dynamically get the like count from the database, return 0 if not available."""
        return obj.like_count() if hasattr(obj, "like_count") else 0

    def get_comment_count(self, obj):
        """Dynamically get the comment count from the database, return 0 if not available."""
        return obj.comment_count() if hasattr(obj, "comment_count") else 0


class LeaderboardLikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # model is the model || LeaderboardLike is the model
        model = LeaderboardLike
        include_fk = True

    leaderboard_image_id = ma.Integer() # leaderboard_image_id is the foreign key || ma is marshmallow || Integer is the type of the field


class LeaderboardCommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # model is the model || LeaderboardComment is the model
        model = LeaderboardComment
        include_fk = True

    leaderboard_image_id = ma.Integer() # leaderboard_image_id is the foreign key || ma is marshmallow || Integer is the type of the field


# Schema instances
leaderboard_schema = LeaderboardSchema()
leaderboards_schema = LeaderboardSchema(many=True)
leaderboard_like_schema = LeaderboardLikeSchema()
leaderboard_comment_schema = LeaderboardCommentSchema()
leaderboard_comments_schema = LeaderboardCommentSchema(many=True)
leaderboard_likes_schema = LeaderboardLikeSchema(many=True)

