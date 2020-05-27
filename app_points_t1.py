from marshmallow_jsonapi import Schema, fields


class Point:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class PointSchema(Schema):
    class Meta:
        type_ = 'points'
        self_view = 'point_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'point_many'

    id = fields.Integer()
    name = fields.Str(required=True)


post = Point(id="1", name="Django is Omakase")
a= PointSchema().dump(post)


exit(0)