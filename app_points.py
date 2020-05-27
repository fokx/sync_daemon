from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

app = Flask(__name__)

# ! DO NOT RUN WITH IDE

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///points.db'
db = SQLAlchemy(app)


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    point = db.Column(db.Float)
    synced = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)


db.create_all()


# Create data abstraction layer
class PointSchema(Schema):
    class Meta:
        type_ = 'points'
        self_view = 'point_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'point_many'

    id = fields.Integer()
    point = fields.Float(required=True)
    synced = fields.Integer()
    timestamp = fields.DateTime(
        required=True, format="%Y-%m-%d %H:%M:%S")
    # "2020-05-02 01:06:47"


@app.route('/')

def example():
    return '{"a":"b"}'
    # return '{"data":{"type":"point", "attributes":{"name":"Salvador Dali", "birth_year":1904, "genre":"Surrealism"}}}'


a = {
    "data": {
        "type": "point",
        "attributes": {
            "name": "Salvador Dali",
            "birth_year": 1904,
            "genre": "Surrealism"
        }
    }
}


class PointMany(ResourceList):
    schema = PointSchema
    data_layer = {'session': db.session,
                  'model': Point}


class PointOne(ResourceDetail):
    schema = PointSchema
    data_layer = {'session': db.session,
                  'model': Point}


api = Api(app)
api.route(PointMany, 'point_many', '/points')
api.route(PointOne, 'point_one', '/points/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=30000)
