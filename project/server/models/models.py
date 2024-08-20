import uuid
from datetime import datetime
from sqlalchemy import ARRAY, JSON, Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from project.server import db


class Blogs(db.Model):
    __tablename__ = 'blogs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    summary = Column(String(500))
    reading_time = Column(String(50))
    thumbnail_url = Column(String(255))
    tags = Column(ARRAY(String))  
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, title, content, author, summary=None, reading_time=None, thumbnail_url=None, tags=None):
        self.title = title
        self.content = content
        self.author = author
        self.summary = summary
        self.reading_time = reading_time
        self.thumbnail_url = thumbnail_url
        self.tags = tags if tags else []

class Users(db.Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    about = Column(String, nullable=True)
    skills = Column(JSON, nullable=True)
    cv_link = Column(String, nullable=True)
    profile_picture_link = Column(String, nullable=True)

    testimonials = db.relationship('Testimonials', backref='author', lazy=True)
    social_media_links = db.relationship('SocialMediaLinks', backref='owner', lazy=True)

    def __init__(self, full_name, username, designation, about=None, skills=None, cv_link=None, profile_picture_link=None):
        self.full_name = full_name
        self.username = username
        self.designation = designation
        self.about = about
        self.skills = skills if skills else []
        self.cv_link = cv_link
        self.profile_picture_link = profile_picture_link

    def __repr__(self):
        return f'<User {self.id} - {self.full_name}>'

class SocialMediaLinks(db.Model):
    __tablename__ = 'social_media_links'  

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)  
    facebook = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    github = Column(String, nullable=True)

    user = db.relationship('Users', backref=db.backref('social_media_links_list', lazy=True))

    def __init__(self, user_id, facebook=None, linkedin=None, instagram=None, github=None):
        self.user_id = user_id
        self.facebook = facebook
        self.linkedin = linkedin
        self.instagram = instagram
        self.github = github

    def __repr__(self):
        return f'<SocialMediaLinks {self.id} - User {self.user_id}>'

class Testimonials(db.Model):
    __tablename__ = 'testimonials' 

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    designation = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    content = Column(String, nullable=False)

    user = db.relationship('Users', backref=db.backref('testimonials_list', lazy=True))

    def __init__(self, user_id, name, company, content, designation=None, date=None):
        self.user_id = user_id
        self.name = name
        self.content = content
        self.designation = designation
        self.company = company
        if date:
            self.date = date

    def __repr__(self):
        return f'<Testimonial {self.id} - {self.name}>'
