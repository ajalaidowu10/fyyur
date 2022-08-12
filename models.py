from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
db = SQLAlchemy()

# TODO: connect to a local postgresql database
def dbsetup(app):
  app.config.from_object('config')
  db.app = app
  db.init_app(app)
  migrate = Migrate(app, db)
  return db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  address = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120), nullable=False)
  image_link = db.Column(db.String(500), nullable=False)
  facebook_link = db.Column(db.String(120), nullable=False)

  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
  website_link = db.Column(db.String(120), nullable=False)
  seeking_description = db.Column(db.String(500), nullable=True)
  seeking_talent = db.Column(db.Boolean, default=False)
  created_at = db.Column(db.DateTime, default=datetime.now())

  shows = db.relationship('Show', backref='venue', lazy=True)
  
  def __repl__(self):
    return f'''
      <Venue 
        {self.id}, 
        {self.name}, 
        {self.city}, 
        {self.state}, 
        {self.address}, 
        {self.phone},
        {self.genres},
        {self.image_link},
        {self.facebook_link}
        {self.website_link},
        {self.seeking_decription},
        {self.seeking_talent},
        {self.created_at}
      >
      '''

class Artist(db.Model):
  __tablename__ = 'artists'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120), nullable=False, unique=True)
  genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
  image_link = db.Column(db.String(500), nullable=False)
  facebook_link = db.Column(db.String(120), nullable=False)

  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  website_link = db.Column(db.String(120), nullable=False)
  seeking_venue = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(500), nullable=True)
  avail_from = db.Column(db.DateTime, nullable=True)
  avail_to = db.Column(db.DateTime, nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.now())

  shows = db.relationship('Show', backref='artist', lazy=True)

  def __repl__(self):
    return f'''
      <Artist
        {self.id},
        {self.name},
        {self.city},
        {self.state},
        {self.phone},
        {self.genres},
        {self.image_link},
        {self.facebook_link},
        {self.website_link},
        {self.seeking_venue},
        {self.seeking_decription},
        {self.created_at}
      >
    '''
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repl__(self):
    return f'''
      <Show
        {self.id},
        {self.artist_id},
        {self.venue_id},
        {self.start_time}
      >
    '''