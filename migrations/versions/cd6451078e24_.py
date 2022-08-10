"""empty message

Revision ID: cd6451078e24
Revises: 
Create Date: 2022-08-06 14:25:48.117626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd6451078e24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    artists_table = op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=False),
    sa.Column('facebook_link', sa.String(length=120), nullable=False),
    sa.Column('website_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    #Seed Artists data
    op.bulk_insert(artists_table, [
        {
            "name": "Guns N Petals",
            "genres": ["Rock n Roll"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "+12326-123-5000",
            "website_link": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        },
        {
          "name": "Matt Quevedo",
          "genres": ["Jazz"],
          "city": "New York",
          "state": "NY",
          "phone": "+234-300-400-5000",
          "website_link": "https://www.mattquevedo.com",
          "facebook_link": "https://www.facebook.com/mattquevedo923251523",
          "seeking_venue": False,
          "seeking_description": '',
          "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        },
        {
          "name": "The Wild Sax Band",
          "genres": ["Jazz", "Classical"],
          "city": "San Francisco",
          "state": "CA",
          "phone": "+234-432-325-5432",
          "facebook_link": "https://www.facebook.com/wildo923251523",
          "website_link": "https://www.wildsex.com",
          "seeking_venue": False,
          "seeking_description": '',
          "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        }
    ])

    venues_table = op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=False),
    sa.Column('facebook_link', sa.String(length=120), nullable=False),
    sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=False),
    sa.Column('website_link', sa.String(length=120), nullable=False),
    sa.Column('seeking_description', sa.String(length=500), nullable=True),
    sa.Column('seeking_talent', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    #Seed Venues data
    op.bulk_insert(venues_table, [
        {
          "name": "The Musical Hop",
          "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
          "address": "1015 Folsom Street",
          "city": "San Francisco",
          "state": "CA",
          "phone": "+235-123-123-1234",
          "website_link": "https://www.themusicalhop.com",
          "facebook_link": "https://www.facebook.com/TheMusicalHop",
          "seeking_talent": True,
          "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
          "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        },
        {
          "name": "The Dueling Pianos Bar",
          "genres": ["Classical", "R&B", "Hip-Hop"],
          "address": "335 Delancey Street",
          "city": "New York",
          "state": "NY",
          "phone": "+222-914-003-1132",
          "website_link": "https://www.theduelingpianos.com",
          "facebook_link": "https://www.facebook.com/theduelingpianos",
          "seeking_talent": False,
          "seeking_description": '',
          "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        },
        {
          "name": "Park Square Live Music & Coffee",
          "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
          "address": "34 Whiskey Moore Ave",
          "city": "San Francisco",
          "state": "CA",
          "phone": "+321-415-000-1234",
          "website_link": "https://www.parksquarelivemusicandcoffee.com",
          "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
          "seeking_talent": False,
          "seeking_description": '',
          "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        }
    ])
    shows_table = op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
    #Seed Shows data
    op.bulk_insert(shows_table, [
        { "artist_id": 1, "venue_id": 1, "start_time": "2019-05-21T21:30:00.000Z"},
        { "artist_id": 2, "venue_id": 3, "start_time": "2019-06-15T23:00:00.000Z"},
        { "artist_id": 3, "venue_id": 3, "start_time": "2035-04-01T20:00:00.000Z"},
        { "artist_id": 3, "venue_id": 3, "start_time": "2035-04-08T20:00:00.000Z"},
        { "artist_id": 3, "venue_id": 3, "start_time": "2035-04-15T20:00:00.000Z"},
    ])
    



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    op.drop_table('venues')
    op.drop_table('artists')
    # ### end Alembic commands ###
