#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment

import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from datetime import datetime
from models import dbsetup, Venue, Show, Artist


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db = dbsetup(app)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  venues = db.session.query(Venue.id, Venue.name).\
                      order_by(Venue.created_at).\
                      limit(10).all();
  artists = db.session.query(Artist.id, Artist.name).\
                      order_by(Artist.created_at).\
                      limit(10).all();
  return render_template('pages/home.html', venues=venues, artists=artists)

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  venue_city = ''
  venues = db.session.query(Venue.id, Venue.name, Venue.city, Venue.state).\
                      order_by(Venue.city, Venue.state).all();
  current_time = datetime.now()
  for venue in venues:
    num_upcoming_shows = db.session.query(Show.id).\
                                    filter(Show.venue_id == venue.id, Show.start_time > current_time).\
                                    count()
    if venue_city != venue.city + venue.state:
        data.append({
          'city': venue.city,
          'state': venue.state,
          'venues': [{
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': num_upcoming_shows
          }]
        })
        venue_city = venue.city + venue.state
    else:
      data[len(data) - 1]['venues'].append({
                                        'id': venue.id,
                                        'name': venue.name,
                                        'num_upcoming_shows': num_upcoming_shows
                                    })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = {}
  current_time = datetime.now()
  search_term = request.form.get('search_term', '')
  search_result = db.session.query(Venue.id, Venue.name).\
                             filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []
  for result in search_result:
    num_upcoming_shows = db.session.query(Show.id).filter(Show.venue_id == result.id, Show.start_time > current_time).\
                        count()
    data.append({
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": num_upcoming_shows
      })

  response['count'] = len(search_result)
  response['data'] = data

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()
  shows = db.session.query(Show.start_time, Show.artist_id, \
                            Artist.name.label('artist_name'), \
                            Artist.image_link.label('artist_image_link')).\
                    join(Artist).filter(Show.venue_id == venue_id).\
                    all()
  for show in shows:
    if show.start_time > current_time:
      upcoming_shows.append({
        'artist_id': show.artist_id,
        'artist_name': show.artist_name,
        'artist_image_link': show.artist_image_link,
        'start_time': str(show.start_time)
        })
    else:
      past_shows.append({
        'artist_id': show.artist_id,
        'artist_name': show.artist_name,
        'artist_image_link': show.artist_image_link,
        'start_time': str(show.start_time)
      })

  setattr(venue, 'past_shows', past_shows)
  setattr(venue, 'upcoming_shows', upcoming_shows)
  setattr(venue, 'past_shows_count', len(past_shows))
  setattr(venue, 'upcoming_shows_count', len(upcoming_shows))

  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  error = False
  try:
    venue = Venue(
                    name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    phone=form.phone.data,
                    address=form.address.data,
                    genres=form.genres.data,
                    image_link=form.image_link.data,
                    website_link=form.website_link.data,
                    facebook_link=form.facebook_link.data,
                    seeking_talent=form.seeking_talent.data,
                    seeking_description=form.seeking_description.data
              )
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error == True:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      return render_template('pages/home.html')
    else:
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error == True:
      flash(f'An error occurred. Venue {venue.name} could not be listed.')
      return "Error", 400
    else:
      flash(f'Venue {venue.name} deleted successfully')
      return "Deleted successfully", 200

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = db.session.query(Artist.id, Artist.name).all()

  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response = {}
  current_time = datetime.now()
  search_term = request.form.get('search_term', '')
  search_result = db.session.query(Artist.id, Artist.name).\
                  filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []
  for result in search_result:
    num_upcoming_shows = db.session.query(Show.id).\
                        filter(Show.artist_id == result.id, Show.start_time > current_time).\
                        count()
    data.append({
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": num_upcoming_shows
      })

  response['count'] = len(search_result)
  response['data'] = data
  return response
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()
  shows = db.session.query(Show.start_time, Show.venue_id, \
                            Venue.name.label('venue_name'), \
                            Venue.image_link.label('venue_image_link')).\
                      join(Venue).filter(Show.artist_id == artist_id).\
                      all()
  for show in shows:
    if show.start_time > current_time:
      upcoming_shows.append({
        'venue_id': show.venue_id,
        'venue_name': show.venue_name,
        'venue_image_link': show.venue_image_link,
        'start_time': str(show.start_time)
        })
    else:
      past_shows.append({
        'venue_id': show.venue_id,
        'venue_name': show.venue_name,
        'venue_image_link': show.venue_image_link,
        'start_time': str(show.start_time)
      })

  setattr(artist, 'past_shows', past_shows)
  setattr(artist, 'upcoming_shows', upcoming_shows)
  setattr(artist, 'past_shows_count', len(past_shows))
  setattr(artist, 'upcoming_shows_count', len(upcoming_shows))
  
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  form = ArtistForm(
          name=artist.name,
          genres=artist.genres,
          city=artist.city,
          state=artist.state,
          phone=artist.phone,
          website_link=artist.website_link,
          facebook_link=artist.facebook_link,
          seeking_venue=artist.seeking_venue,
          seeking_description=artist.seeking_description,
          image_link=artist.image_link,
          avail_to=artist.avail_to,
          avail_from=artist.avail_from
      )
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  error = False
  try:
    artist = Artist.query.get(artist_id);
    artist.name=form.name.data
    artist.city=form.city.data
    artist.state=form.state.data
    artist.phone=form.phone.data
    artist.genres=form.genres.data
    artist.image_link=form.image_link.data
    artist.website_link=form.website_link.data
    artist.facebook_link=form.facebook_link.data
    artist.seeking_venue=form.seeking_venue.data
    artist.seeking_description=form.seeking_description.data

    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error == True:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
      return render_template('forms/edit_artist.html', form=form, artist=artist)
    else:
      flash('Artist ' + request.form['name'] + ' was successfully updated!')
      return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id);
  form = VenueForm(
          name=venue.name,
          genres=venue.genres,
          city=venue.city,
          state=venue.state,
          phone=venue.phone,
          address=venue.address,
          website_link=venue.website_link,
          facebook_link=venue.facebook_link,
          seeking_talent=venue.seeking_talent,
          seeking_description=venue.seeking_description,
          image_link=venue.image_link
      )
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  error = False
  try:
    venue = Venue.query.get(venue_id);
    venue.name=form.name.data
    venue.city=form.city.data
    venue.state=form.state.data
    venue.phone=form.phone.data
    venue.address=form.address.data
    venue.genres=form.genres.data
    venue.image_link=form.image_link.data
    venue.website_link=form.website_link.data
    venue.facebook_link=form.facebook_link.data
    venue.seeking_talent=form.seeking_talent.data
    venue.seeking_description=form.seeking_description.data

    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error == True:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
      return render_template('pages/edit_venue.html')
    else:
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
      return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm()
  error = False
  try:
    artist = Artist(
                    name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    phone=form.phone.data,
                    genres=form.genres.data,
                    image_link=form.image_link.data,
                    website_link=form.website_link.data,
                    facebook_link=form.facebook_link.data,
                    seeking_venue=form.seeking_venue.data,
                    seeking_description=form.seeking_description.data,
                    avail_from=form.avail_from.data,
                    avail_to=form.avail_to.data
              )
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error == True:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      return render_template('pages/home.html')
    else:
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html', form=form)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = db.session.query(Show.start_time, Show.venue_id, Show.artist_id, \
                            Venue.name.label('venue_name'), \
                            Artist.name.label('artist_name'), \
                            Artist.image_link.label('artist_image_link')).\
                      join(Artist, Venue).all()
  data = []
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue_name,
      "artist_id": show.artist_id,
      "artist_name": show.artist_name,
      "artist_image_link": show.artist_image_link,
      "start_time": str(show.start_time)
      })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm()
  error = False
  error_message = 'An error occurred. Show could not be listed.'
  try:
    check_artist = db.session.query(Artist.id).filter(Artist.id == form.artist_id.data, \
                        Artist.avail_from <= form.start_time.data, \
                        Artist.avail_to >= form.start_time.data ).count()
    if check_artist == 0:
      error_message = "Sorry Artist is not available at this time"
      raise Exception(error_message)
    show = Show(
                    venue_id=form.venue_id.data,
                    artist_id=form.artist_id.data,
                    start_time=form.start_time.data,
              )

    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error == True:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash(error_message)
      return render_template('pages/home.html')
    else:
      # on successful db insert, flash success
      flash('Show was successfully listed!')
      return render_template('pages/home.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
