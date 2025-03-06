from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
    dob = fields.Date()
    profile_image = fields.Str()
    password = fields.Str(required=True, load_only=True)

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    image_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    content = fields.Str(required=True)

class LikeSchema(Schema):
    id = fields.Int(dump_only=True)
    image_id = fields.Int(required=True)
    user_id = fields.Int(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
comment_schema = CommentSchema()
like_schema = LikeSchema()


# Schema for login
class LoginSchema(Schema):
    email = fields.Email(required=True)  # Email is required
    password = fields.String(required=True, load_only=True)  # Password is required and hidden from response


# Init schema for login
login_schema = LoginSchema()



# from marshmallow import Schema, fields
# from app.extensions import ma
# from app.models import Users


# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         # model is the model || Users is the model
#         model = Users
#         include_fk = True  # Include foreign keys

#     dob = fields.Date(format="%Y-%m-%d", allow_none=True)  # ✅ Allow `dob` to be None
#     phone = fields.String(allow_none=True)  # ✅ Allow `phone` to be None
#     password = ma.auto_field(load_only=True)  # Hide password from responses


# # Init schema for single and multiple users
# user_schema = UserSchema() # Single user || user_schema is an instance of UserSchema class || UserSchema is a class that generates a schema from a SQLAlchemy model
# users_schema = UserSchema(many=True) # Multiple users || users_schema is an instance of UserSchema class || UserSchema is a class that generates a schema from a SQLAlchemy model 