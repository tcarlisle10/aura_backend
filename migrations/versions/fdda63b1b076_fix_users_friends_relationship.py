"""Fix Users.friends relationship

Revision ID: fdda63b1b076
Revises: 
Create Date: 2025-03-05 22:25:06.549178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdda63b1b076'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('friends', schema=None) as batch_op:
        batch_op.drop_constraint('friends_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('friends_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['friend_id'], ['id'])
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_constraint('images_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.drop_constraint('leaderboard_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('leaderboard_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'images', ['original_image_id'], ['id'])
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    with op.batch_alter_table('leaderboard_comments', schema=None) as batch_op:
        batch_op.drop_constraint('leaderboard_comments_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('leaderboard_comments_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'leaderboard', ['leaderboard_image_id'], ['id'])

    with op.batch_alter_table('leaderboard_likes', schema=None) as batch_op:
        batch_op.drop_constraint('leaderboard_likes_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('leaderboard_likes_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'leaderboard', ['leaderboard_image_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leaderboard_likes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('leaderboard_likes_ibfk_2', 'leaderboard', ['leaderboard_image_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('leaderboard_likes_ibfk_1', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('leaderboard_comments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('leaderboard_comments_ibfk_1', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('leaderboard_comments_ibfk_2', 'leaderboard', ['leaderboard_image_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('leaderboard_ibfk_2', 'images', ['original_image_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('leaderboard_ibfk_1', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('images_ibfk_1', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('friends', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('friends_ibfk_1', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('friends_ibfk_2', 'users', ['friend_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###
