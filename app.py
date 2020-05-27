from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

app = Flask(__name__)

# ! DO NOT RUN WITH IDE

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artists.db'
db = SQLAlchemy(app)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birth_year = db.Column(db.Integer)
    genre = db.Column(db.String)


db.create_all()


# Create data abstraction layer
class ArtistSchema(Schema):
    class Meta:
        type_ = 'artist'
        self_view = 'artist_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'artist_many'

    id = fields.Integer()
    name = fields.Str(required=True)
    birth_year = fields.Integer(load_only=True)
    genre = fields.Str()


@app.route('/')
def example():
    return '{"a":"b"}'
    # return '{"data":{"type":"artist", "attributes":{"name":"Salvador Dali", "birth_year":1904, "genre":"Surrealism"}}}'


a = {
    "data": {
        "type": "artist",
        "attributes": {
            "name": "Salvador Dali",
            "birth_year": 1904,
            "genre": "Surrealism"
        }
    }
}


class ArtistMany(ResourceList):
    schema = ArtistSchema
    data_layer = {'session': db.session,
                  'model': Artist}


class ArtistOne(ResourceDetail):
    schema = ArtistSchema
    data_layer = {'session': db.session,
                  'model': Artist}


api = Api(app)
api.route(ArtistMany, 'artist_many', '/artists')
api.route(ArtistOne, 'artist_one', '/artists/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=30000)
