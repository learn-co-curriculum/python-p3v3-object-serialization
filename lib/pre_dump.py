# lib/pre_dump.py

from pprint import pprint
from marshmallow import Schema, fields, pre_dump

# model

class Album():
    def __init__(self, title, artist, num_sold):
        self.title = title
        self.artist = artist
        self.num_sold = num_sold
    
# schema 

class AlbumSchema(Schema):
    title = fields.Str()
    artist = fields.Str()
    num_sold = fields.Int()
    big_hit = fields.Bool()
    
    # compute field prior to serialization
    @pre_dump()
    def get_data(self, data, **kwargs):
        data.big_hit = data.num_sold > 1000000
        return data
    
# create model and schema instances
album_1 = Album("The Wall", "Pink Floyd", 19000000)
album_2 = Album("Renaissance", "Beyonce", 332000)
schema = AlbumSchema() 

# deserialize model instances

pprint(schema.dumps(album_1))
# => '{"title": "The Wall", "artist": "Pink Floyd", "num_sold": 19000000, "big_hit": true}'

pprint(schema.dumps(album_2))
# => '{"title": "Renaissance", "artist": "Beyonce", "num_sold": 332000, "big_hit": 'false}'