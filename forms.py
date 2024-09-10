"""Forms for playlist app."""

from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField("Playlist Name", validators=[InputRequired(), Length(max=100)])
    description = StringField("Description", validators=[Length(max=255)])


class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField("Song Title", validators=[InputRequired(), Length(max=100)])
    artist = StringField("Artist", validators=[InputRequired(), Length(max=100)])


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
