from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Initialize the database and create tables
connect_db(app)
with app.app_context():
    db.create_all()

# Debug Toolbar
debug = DebugToolbarExtension(app)

@app.route("/")
def root():
    """Homepage: redirect to /playlists."""
    return redirect("/playlists")

##############################################################################
# Playlist routes

@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""
    playlists = Playlist.query.all()
    # NEW line of code create a form instance
    form = PlaylistForm() 
    return render_template("playlists.html", playlists=playlists, form=form)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template("playlist.html", playlist=playlist)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    playlist = Playlist.query.all()
    form = PlaylistForm()

    if form.validate_on_submit():
        new_playlist = Playlist(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(new_playlist)
        db.session.commit()
        print("gud job")
        return redirect("/playlists")

    return render_template("new_playlist.html", form=form)

##############################################################################
# Song routes

@app.route("/songs")
def show_all_songs():
    """Show list of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Return a specific song."""
    song = Song.query.get_or_404(song_id)
    return render_template("song.html", song=song)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add song to SQLA and redirect to list-of-songs
    """
    form = SongForm()

    if form.validate_on_submit():
        new_song = Song(
            title=form.title.data,
            artist=form.artist.data
        )
        db.session.add(new_song)
        db.session.commit()
        return redirect("/songs")

    return render_template("new_song.html", form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist and redirect to playlist detail page."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = (db.session.query(Song.id, Song.title)
                         .filter(Song.id.notin_(curr_on_playlist))
                         .all())
    form.song.choices = [(song.id, song.title) for song in available_songs]

    if form.validate_on_submit():
        # Create a PlaylistSong association between the song and the playlist
        playlist_song = PlaylistSong(song_id=form.song.data,
                                     playlist_id=playlist_id)
        db.session.add(playlist_song)
        db.session.commit()

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                           playlist=playlist,
                           form=form)
