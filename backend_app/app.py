from flask import Flask, request, jsonify
from config import Config
from models import db, Songs

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# API to get all songs or paginated songs
@app.route('/api/songs', methods=['GET'])
def get_songs():
    try:
        # Get page and per_page from query parameters
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', type=int)

        # Check if pagination is required
        if page is None and per_page is None:
            # Fetch all songs if no pagination parameters are provided
            songs = Songs.query.all()
            return jsonify({
                'status': 'Success',
                'data': [{
                    'id': song.id,
                    'title': song.title,
                    'danceability': song.danceability,
                    'energy': song.energy,
                    'key': song.key,
                    'loudness': song.loudness,
                    'mode': song.mode,
                    'acousticness': song.acousticness,
                    'instrumentalness': "{:.10f}".format(song.instrumentalness),
                    'liveness': song.liveness,
                    'valence': song.valence,
                    'tempo': song.tempo,
                    'duration_ms': song.duration_ms,
                    'time_signature': song.time_signature,
                    'num_bars': song.num_bars,
                    'num_sections': song.num_sections,
                    'num_segments': song.num_segments,
                    'classes': song.classes,
                    'star_rating': song.star_rating
                } for song in songs]
            }), 200

        # Default to page 1 and per_page 10 if pagination parameters are present but invalid
        page = page if page is not None else 1
        per_page = per_page if per_page is not None else 10

        # Fetch the songs with pagination
        songs = Songs.query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'status': 'Success',
            'total': songs.total,
            'pages': songs.pages,
            'page': songs.page,
            'per_page': songs.per_page,
            'data': [{
                'id': song.id,
                'title': song.title,
                'danceability': song.danceability,
                'energy': song.energy,
                'key': song.key,
                'loudness': song.loudness,
                'mode': song.mode,
                'acousticness': song.acousticness,
                'instrumentalness': "{:.10f}".format(song.instrumentalness),
                'liveness': song.liveness,
                'valence': song.valence,
                'tempo': song.tempo,
                'duration_ms': song.duration_ms,
                'time_signature': song.time_signature,
                'num_bars': song.num_bars,
                'num_sections': song.num_sections,
                'num_segments': song.num_segments,
                'classes': song.classes,
                'star_rating': song.star_rating
            } for song in songs]
        }), 200

    except Exception as e:
        return jsonify({'status': 'Failed', 'message': str(e)}), 500

# API to get song by title
@app.route('/api/songs/<string:title>', methods=['GET'])
def get_song_by_title(title):
    try:
        # Query the Songs table for the first song with the given title
        song = Songs.query.filter_by(title=title.strip()).first()
        if song:
            return jsonify({
                'status': 'Success',
                'data': {
                    'id': song.id,
                    'title': song.title,
                    'danceability': song.danceability,
                    'energy': song.energy,
                    'key': song.key,
                    'loudness': song.loudness,
                    'mode': song.mode,
                    'acousticness': song.acousticness,
                    'instrumentalness': "{:.10f}".format(song.instrumentalness),
                    'liveness': song.liveness,
                    'valence': song.valence,
                    'tempo': song.tempo,
                    'duration_ms': song.duration_ms,
                    'time_signature': song.time_signature,
                    'num_bars': song.num_bars,
                    'num_sections': song.num_sections,
                    'num_segments': song.num_segments,
                    'classes': song.classes,
                    'star_rating': song.star_rating
                }
            }), 200
        else:
            return jsonify({'status': 'Failed', 'message': 'Song not found'}), 404
    except Exception as e:
        return jsonify({'status': 'Failed', 'message': str(e)}), 500

# API to rate a song
@app.route('/api/songs/rate/<string:id>', methods=['PUT'])
def rate_song(id):
    try:
        # Fetch the song by its ID
        song = db.session.get(Songs, id.strip())
        if not song:
            return jsonify({'status': 'Failed', 'message': 'Song not found'}), 404

        # Validate that the star rating is between 1 and 5
        star_rating = request.json.get('star_rating')
        if not 1 <= star_rating <= 5:
            return jsonify({'status': 'Failed', 'message': 'Rating must be between 1 and 5'}), 400

        # Update the star rating for the song
        song.star_rating = star_rating
        db.session.commit()
        return jsonify({'status': 'Success', 'message': 'Song rated successfully'}), 200

    except Exception as e:
        return jsonify({'status': 'Failed', 'message': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
