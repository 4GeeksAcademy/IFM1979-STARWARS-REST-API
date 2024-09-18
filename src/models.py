from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_character = db.Table('favorite_character',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True)
)

favorite_planet = db.Table('favorite_planet',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
   
   
    favorite_planet = db.relationship('Planet', secondary='favorite_planet', backref=db.backref('user'))
    favorite_character = db.relationship('Character', secondary='favorite_character', backref=db.backref('user'))
    

    def __repr__(self):
        return '<User %r>' % self.email


    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    species = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
   
    def __repr__(self):
        return '<Character %r>' % self.name


    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "species": self.species,
            "homeworld":self.homeworld,
    }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    population = db.Column(db.Integer)
   
    def __repr__(self):
        return '<Planet %r>' % self.name


    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "climate": self.climate,
            "terrain":self.terrain,
            "population":self.population,
    }





