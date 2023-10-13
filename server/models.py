from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Movie(db.Model, SerializerMixin):
    __tablename__='movie_table'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    rating = db.Column(db.Integer)
    description = db.Column(db.String)

    # Add relationship
    credits = db.relationship("Credit", backref="movie")

    #Add Validations
    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <= 10:
            raise ValueError("Rating must be between 1 and 10!")
        return rating

    @validates('genre')
    def validate_genre(self, key, genre):
        GENRES = [ "Action", "Comedy", "Drama", "Horror", "Romance", "Thriller", "Science Fiction", "Fantasy", "Mystery", "Adventure", "Crime", "Family", "Animation", "Documentary", "War"]
        if genre not in GENRES:
            return ValueError (f'Genre must be one of the following: {GENRES}')
        return genre

class Actor(db.Model, SerializerMixin):
    __tablename__='actor_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    credits = db.relationship("Credit", backref="actor")

    # Add validation
    @validates('age')
    def validate_age(self, key, age):
        if not age > 10:
            raise ValueError("Age must be greater than 10!")
        return age

class Credit(db.Model, SerializerMixin):
    __tablename__='credit_table'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False)

    # Add relationship
    actor_id = db.Column(db.Integer, db.ForeignKey('actor_table.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_table.id'), nullable=False)
    
    # Add serialization rules
    serialize_rules = ('-movie', '-actor')

     # Add validation
    @validates('role')
    def validate_role(self, key, role):
        ROLES=["Performer", "Director", "Producor", "Playwright", "Lighting Design", "Sound Design", "Set Design"]
        if role not in ROLES:
            return ValueError (f'Role must be one of the following: {ROLES}')
        return role

# class Movie(db.Model, SerializerMixin):
#     tablename='movie_table'

#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.String)
#     title = db.Column(db.String)
#     genre = db.Column(db.String)
#     rating = db.Column(db.Integer)
#     description = db.Column(db.String)

#     credits = db.relationship("Credit", backref = 'movie', cascade = 'all,delete-orphan')

# class Actor(db.Model, SerializerMixin):
#     tablename='actor_table'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     age = db.Column(db.Integer)

#     credits = db.relationship("Credit", backref = "actor", cascade = 'all,delete-orphan')

#     @validates('name', 'age')
#     def validate_name_age(self, key, name, age):
#         if name and name is name and age > 10:
#             return name, age
#         else:
#             raise ValueError('Not a valid  name or age')


# class Credit(db.Model, SerializerMixin):
#     tablename='credit_table'

#     id = db.Column(db.Integer, primary_key = True)
#     role = db.Column(db.String)

#     actor_id = db.Column(db.Integer, db.ForeignKey('actor_table.id'))
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie_table.id'))

#     serialize_rules = ('-actor', '-movie')

#     @validates('role')
#     def validate_role(self, key, role):
#         roles = ["Performer", "Director", "Producor", "Playwright", "Lighting Design", "Sound Design", "Set Design"]
#         if role not in roles:
#             return ValueError(f'role must be one of the following:{roles}')
#         return role