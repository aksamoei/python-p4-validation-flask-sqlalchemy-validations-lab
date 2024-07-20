from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, the_name):
        if len(the_name) < 1 or Author.query.filter_by(name=the_name).first():
            raise ValueError("invalid input name")
        else: 
            return the_name

    @validates('phone_number')
    def validate_phone(self, key, numb):
        if len(numb) == 10 and numb.isdigit():
            return numb
        else:
            raise ValueError("Phone number must be 10 digits")


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, the_title):
        if len(the_title) < 1 or not any(word in the_title for word in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError('Title should not be empty')
        else:
            return the_title
    
    @validates('summary')
    def validate_summary(self, key, the_summary):
        if len(the_summary) > 250:
            raise ValueError('Summary should not exceed 250 chars')
        else:
            return the_summary


    @validates('content')
    def validate_content(self, key, the_content):
        if len(the_content) < 250:
            raise ValueError('Less than 250 chars.')
        else:
            return the_content
        
    @validates('category')
    def validate_category(self, key, category):
        if category not in ('Fiction', 'Non-Fiction'):
            raise ValueError('Category must be either fiction or non-fiction')
        else:
            return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
