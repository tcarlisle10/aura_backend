from datetime import date
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=True)
    dob: Mapped[date] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(db.String(500), nullable=False)

    images: Mapped[List['Images']] = relationship('Images', back_populates='user')
    leaderboard_images: Mapped[List['Leaderboard']] = relationship('Leaderboard', back_populates='user')
    comments: Mapped[List['LeaderboardComment']] = relationship('LeaderboardComment', back_populates='user')
    likes: Mapped[List['LeaderboardLike']] = relationship('LeaderboardLike', back_populates='user')

    
    friends = relationship(
        "Users",
        secondary="friends",
        primaryjoin="Users.id == Friends.user_id",
        secondaryjoin="Users.id == Friends.friend_id",
        backref="friend_of"
    )

class Images(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True)
    image_path: Mapped[str] = mapped_column(db.String(255), nullable=False)  # Store path instead of binary
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))

    user: Mapped['Users'] = relationship('Users', back_populates='images')
    leaderboard: Mapped[List['Leaderboard']] = relationship('Leaderboard', back_populates='original_image')

class Leaderboard(Base):
    __tablename__ = 'leaderboard'

    id: Mapped[int] = mapped_column(primary_key=True)
    image_path: Mapped[str] = mapped_column(db.String(255), nullable=False)  # Store path instead of binary
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    original_image_id: Mapped[int] = mapped_column(db.ForeignKey('images.id'))

    user: Mapped['Users'] = relationship('Users', back_populates='leaderboard_images')
    original_image: Mapped['Images'] = relationship('Images', back_populates='leaderboard')

    comments: Mapped[List['LeaderboardComment']] = relationship(
        'LeaderboardComment', back_populates='leaderboard_image', cascade="all, delete-orphan"
    )
    likes: Mapped[List['LeaderboardLike']] = relationship(
        'LeaderboardLike', back_populates='leaderboard_image', cascade="all, delete-orphan"
    )

    def like_count(self):
        """Get the total number of likes dynamically."""
        return db.session.query(LeaderboardLike).filter_by(leaderboard_image_id=self.id).count()

    def comment_count(self): 
        """Get the total number of comments dynamically."""
        return db.session.query(LeaderboardComment).filter_by(leaderboard_image_id=self.id).count()

class LeaderboardComment(Base):
    __tablename__ = 'leaderboard_comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(db.String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), nullable=False)
    leaderboard_image_id: Mapped[int] = mapped_column(db.ForeignKey('leaderboard.id'), nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='comments')
    leaderboard_image: Mapped['Leaderboard'] = relationship('Leaderboard', back_populates='comments')

class LeaderboardLike(Base):
    __tablename__ = 'leaderboard_likes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    leaderboard_image_id: Mapped[int] = mapped_column(db.ForeignKey('leaderboard.id'))

    user: Mapped['Users'] = relationship('Users', back_populates='likes')
    leaderboard_image: Mapped['Leaderboard'] = relationship('Leaderboard', back_populates='likes')

class Friends(Base):
    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    friend_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))

    
    user: Mapped['Users'] = relationship('Users', foreign_keys=[user_id])
    friend: Mapped['Users'] = relationship('Users', foreign_keys=[friend_id])



