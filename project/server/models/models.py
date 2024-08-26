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
    cv_link = Column(String, nullable=True)
    profile_picture_link = Column(String, nullable=True)

    testimonials = db.relationship('Testimonials', backref='user_testimonials', lazy=True)
    social_media_links = db.relationship('SocialMediaLinks', backref='user_social_links', lazy=True)
    user_skills = db.relationship('UserSkills', backref='user_skills', lazy=True)
    education = db.relationship('Education', backref='user_education', lazy=True, cascade="all, delete-orphan")
    experience = db.relationship('Experience', backref='user_experience', lazy=True, cascade="all, delete-orphan")

    def __init__(self, full_name, username, designation, about=None, skills=None, cv_link=None, profile_picture_link=None):
        self.full_name = full_name
        self.username = username
        self.designation = designation
        self.about = about
        self.cv_link = cv_link
        self.profile_picture_link = profile_picture_link

    def __repr__(self):
        return f'<User {self.id} - {self.full_name}>'


class UserSkills(db.Model):
    __tablename__ = 'user_skills'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    skill = Column(String(255), nullable=False)
    icon_link = Column(String(255), nullable=False)

    user = db.relationship('Users', backref=db.backref('skills', lazy=True))

    def __init__(self, user_id, skill, icon_link):
        self.user_id = user_id
        self.skill = skill
        self.icon_link = icon_link

    def __repr__(self):
        return f'<UserSkills {self.id} - {self.skill}>'
    
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
    image_link = Column(String(255), nullable=True)

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


class Education(db.Model):
    __tablename__ = 'education'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    year = db.Column(db.String(255), nullable=False)
    degree = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(255), nullable=False)
    cgpa = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, year, degree, university, cgpa):
        self.user_id = user_id
        self.year = year
        self.degree = degree
        self.university = university
        self.cgpa = cgpa



class Experience(db.Model):
    __tablename__ = 'experience'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    year = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    work_details = db.Column(ARRAY(db.String), nullable=True)

    def __init__(self, user_id, year, position, company, work_details):
        self.user_id = user_id
        self.year = year
        self.position = position
        self.company = company
        self.work_details = work_details