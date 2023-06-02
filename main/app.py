from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///zgm.db"
db = SQLAlchemy(app)

app.app_context().push()
db.create_all()

tracks = db.Table('TRACKS', db.metadata, autoload_with=db.engine)
artists = db.Table('ARTISTS',db.metadata, autoload_with=db.engine)

today = datetime.date.today()
current_time = datetime.datetime.now()
last_monday = today - datetime.timedelta(days=today.weekday())

# with app.app_context():
#     db.create_all()


@app.route("/")
@app.route("/home")
def Home():
    first_row = db.session.query(tracks).filter(tracks.c.RANK < 6).order_by(tracks.c.RANK.asc())
    second_row = db.session.query(tracks).filter((tracks.c.RANK > 5)&(tracks.c.RANK < 11)).order_by(tracks.c.RANK.asc())
    top_song = db.session.query(tracks).filter(tracks.c.RANK < 2).first()
    return render_template('home.html', posts=first_row, post1=second_row ,post2=last_monday, post3=top_song, post4=today, clock=current_time)


@app.route("/charts")
@app.route("/ZGcharts")
def Charts():
    ranks = db.session.query(tracks).filter(tracks.c.RANK < 11).order_by(tracks.c.RANK.asc())
    return render_template('charts.html', title='ZG Top 10', posts=ranks, post2=last_monday, clock=current_time)


@app.route("/cucharts")
def CUrank():
    curanks = db.session.query(tracks).filter(tracks.c.CURANK < 31).order_by(tracks.c.CURANK.asc())
    return render_template('cucharts.html', title='CU Top 30', posts=curanks, post2=last_monday, clock=current_time)


@app.route("/artists")
def Artists():
    profile = db.session.query(artists).all()
    return render_template('artists.html', title='Artists', posts=profile, clock=current_time)

@app.route("/playlists")
def Playlist():
    return render_template('playlist.html', title='Playlists', clock=current_time)

if __name__ == '__main__':
    app.run(debug=True)






