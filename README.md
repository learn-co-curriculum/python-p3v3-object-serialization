# Serialization : Code-Along

## Learning Goals

- Use the marshmallow library to convert Python objects to primitive Python data
  types.

---

## Key Vocab

- **Serialization**: a process to convert programmatic data such as a Python
  object to a sequence of bytes that can be shared with other programs,
  computers, or networks.
- **Deserialization**: the reverse process, converting input data back to
  programmatic data.
- **Validation**: a process for checking the validity of data such as the type,
  format, or values.
- **Schema**: A class used to validate, serialize, and deserialize data.

---

## Introduction

We often need to convert data from one data structure to another. For example,
we may want to convert a complex Python object to a dictionary with native
Python data types as values, or vice versa.

Serialization is a technique for converting data such as a Python object into a
series of bytes. When a Python object is serialized, we can share it with other
programs, computers, or networks. Deserialization is the reverse process,
converting the byte stream back to an object. Validation is a process of
checking the validity of data such as the type, format, or values. Validation is
usually part of deserialization, but could be done during serialization as well.

The `marshmallow` library is a powerful tool for serializing, deserializing, and
validating data in Python. It is also database and platform agnostic, which
makes useful in many applications.

In this lesson, we'll use learn how to use `marshmallow` to serialize a Python
object. While there are different formats for data serialization, we will
primarily serialize a Python object to either a dictionary or a JSON-encoded
string.

---

## Setup

This lesson is a code-along, so fork and clone the repo.

Run `pipenv install` to install the dependencies and `pipenv shell` to enter
your virtual environment before running your code.

```console
$ pipenv install
$ pipenv shell
```

---

### Defining a schema

A marshmallow **schema** is used to:

- Validate input data.
- Deserialize input data to application-level objects.
- Serialize application-level objects to primitive Python types.

Within the `lib` directory, you'll find the file `serialize.py` that defines a
simple `Dog` class . We will refer to a class that defines the structure of an
object that we wish to serialize as a **model**. Notice we have a new import
`pprint`, which provides support to recursively pretty-print lists, tuples, and
dictionaries.

```py
# lib/serialize.py

from pprint import pprint

# model

class Dog:
    def __init__(self, name, breed, tail_wagging = False):
        self.name = name
        self.breed = breed
        self.tail_wagging = tail_wagging

# create model instance

dog = Dog(name="Snuggles", breed="Beagle", tail_wagging=True)
print(dog)
```

If you run the code, you'll see output that indicates something about the
object's memory location:

```console
$ python lib/serialize.py
<__main__.Dog object at 0x100826810>
```

To print the state of the `Dog` object in a format that is easy to read, we will
define a `marshmallow` schema named `DogSchema` and then use an instance of that
schema to serialize the object.

Edit the code as shown below to define the `DogSchema` class and create an
instance of the class. You will also need to add a new import statement.

```py
# lib/serialize.py

from pprint import pprint
from marshmallow import Schema, fields

# model

class Dog:
    def __init__(self, name, breed, tail_wagging = False):
        self.name = name
        self.breed = breed
        self.tail_wagging = tail_wagging

    def give_treat(self):
        self.tail_wagging = True

    def scold(self):
        self.tail_wagging = False

# schema

class DogSchema(Schema):
    name = fields.Str()
    breed = fields.Str()
    tail_wagging = fields.Boolean()

# create model and schema instances

dog = Dog(name="Snuggles", breed="Beagle", tail_wagging=True)
dog_schema = DogSchema()
```

- `Schema` and `fields` are imported from the `marshmallow` library.
- `DogSchema` defines the same 3 fields as the `Dog` model class. Each field is
  assigned a marshmallow type.

The `DogSchema` instance can be used to serialize the state of the `Dog`
instance. We'll do that using two inherited methods for dumping object state:

- `dump()` serializes an object to a dictionary
- `dumps()` serializes an object to a JSON-encoded string

### Serializing/dumping to a dictionary using `dump()`

Let's first serialize the `Dog` instance to a dictionary using the `dump()`
method and pretty-print the result. Add the following to the code:

```py
# serialize object to dictionary with schema.dump()

dog_dict = dog_schema.dump(dog)
pprint(dog_dict)
# => {'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True}
```

Run the code to see the dog's fields printed as a dictionary with the fields as
keys:

```console
$ python lib/serialize.py
{'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True}
```

### Serializing/dumping to JSON using `dumps()`

We can also serialize to a JSON-encoded string using `dumps()`. Update the code
to add the following:

```py
# serialize object to JSON-encoded string with schema.dumps()

dog_json = dog_schema.dumps(dog)
pprint(dog_json)
# => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
```

Run the code again and confirm an additional line of output containing a
JSON-encoded string for the fields and values. Notice the JSON data contains the
boolean value `true` instead of the Python value `True`.

```console
'{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
```

### Filtering

We can specify which fields to output by passing either an `only` or an
`exclude` parameter to the dump methods. Each parameter takes a tuple of strings
corresponding to field names. For example:

```py
# specify which fields to output with the only parameter, passed as a tuple.

dog_summary = DogSchema(only=("name", "breed")).dumps(dog)
pprint(dog_summary)
# => '{"name": "Snuggles", "breed": "Beagle"}'

# omit fields by passing the exclude parameter (note the comma in the single-value tuple).

dog_summary = DogSchema(exclude=("tail_wagging", )).dumps(dog)
pprint(dog_summary)
# => '{"name": "Snuggles", "breed": "Beagle"}'
```

### Serialize a collection

A collection can be serialized by instantiating the schema with the parameter
`many=True`. The `dump()` method returns a list of dictionaries, while the
`dumps()` method returns a string containing a JSON array literal.

Update the code to serialize a list of `Dog` instances as shown:

```py
# serialize a collection with many=True

dogs = [Dog(name="Snuggles", breed="Beagle", tail_wagging=True),
        Dog(name="Wags", breed = "Collie", tail_wagging=False)]
dictionary_list = DogSchema(many=True).dump(dogs)   # dump returns list of dictionaries
pprint(dictionary_list)
# => [{'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True},
# =>  {'breed': 'Collie', 'name': 'Wags', 'tail_wagging': False}]

json_array = DogSchema(many=True).dumps(dogs)       # dumps returns JSON-encoded array
pprint(json_array)   # NOTE: String is enclosed in parenthesis to print across multiple lines
# => ('[{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}, {"name": '
# =>  '"Wags", "breed": "Collie", "tail_wagging": false}]')
```

### Pre-dump processing

The marshmallow library provides decorators for registering schema
pre-processing and post-processing methods. We define a method to execute prior
to serialization using the `@pre_dump` decorator and after serialization using
`@post_dump`.

Consider the code in `lib/pre_dump.py`, which defines an `Album` model and
corresponding schema named `AlbumSchema`. We can easily created and serialize
model instances as shown:

```py
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
    title = fields.Str(required=True)
    artist = fields.Str(required=True)
    num_sold = fields.Int(required=True)

# create model and schema instances
album_1 = Album("The Wall", "Pink Floyd", 19000000)
album_2 = Album("Renaissance", "Beyonce", 332000)
schema = AlbumSchema()

# deserialize model instances

pprint(schema.dumps(album_1))
# => '{"title": "The Wall", "artist": "Pink Floyd", "num_sold": 19000000}'

pprint(schema.dumps(album_2))
# => '{"title": "Renaissance", "artist": "Beyonce", "num_sold": 332000}'
```

Let's supposed we would like to include in the serialized output a boolean named
`big_hit` that indicates if the album sold more than a million copies. We'll add
a field named `big_hit` to the schema, along with a method decorated with
`@pre_dump()` that assigns a value based on the `num_sold` field. The method
receives the object to be serialized and returns the processed object.

```py
class AlbumSchema(Schema):
    title = fields.Str(required=True)
    artist = fields.Str(required=True)
    num_sold = fields.Int(required=True)
    big_hit = fields.Bool(dump_only = True)

    # compute field prior to serialization
    @pre_dump()
    def get_data(self, data, **kwargs):
        data.big_hit = data.num_sold > 1000000
        return data
```

Run the code again to confirm the `big_hit` field is included in the serialized
result. Recall that Python may print a long string across multiple lines by
enclosing it in parenthesis.

```console
$ python lib/pre_dump.py
('{"title": "The Wall", "artist": "Pink Floyd", "num_sold": 19000000, '
 '"big_hit": true}')
('{"title": "Renaissance", "artist": "Beyonce", "num_sold": 332000, "big_hit": '
 'false}')
```

Let's update the comments to reflect the new output:

```py
# deserialize model instances

pprint(schema.dumps(album_1))
# => '{"title": "The Wall", "artist": "Pink Floyd", "num_sold": 19000000, "big_hit": true}'

pprint(schema.dumps(album_2))
# => '{"title": "Renaissance", "artist": "Beyonce", "num_sold": 332000, "big_hit": 'false}'
```

## Conclusion

Serialization is a technique for turning objects into simple, portable formats.
The `marshmallow` library makes it easy to convert a Python object into a
dictionary or JSON-encoded string.

- A **schema** defines fields to validate, serialize, and deserialize data.
- The schema `dump()` method serializes an object to a dictionary.
- The schema `dumps()` method serializes an object to a JSON-encoded string.
- A schema can serialize a collection by passing `many=True` as a parameter
  either during schema instantiation or dumping.
- We define methods to execute prior to serialization using the `@pre_dump`
  decorator and after serialization using `@post_dump`.

---

### Solution Code

```py
# lib/serialize.py

from pprint import pprint
from marshmallow import Schema, fields

# model

class Dog:
    def __init__(self, name, breed, tail_wagging = False):
        self.name = name
        self.breed = breed
        self.tail_wagging = tail_wagging

    def give_treat(self):
        self.tail_wagging = True

    def scold(self):
        self.tail_wagging = False

# schema

class DogSchema(Schema):
    name = fields.Str()
    breed = fields.Str()
    tail_wagging = fields.Boolean()

# create schema and model instances

dog_schema = DogSchema()
dog = Dog(name="Snuggles", breed="Beagle", tail_wagging=True)

# serialize object to dictionary with schema.dump()

dog_dict = dog_schema.dump(dog)
pprint(dog_dict)
# => {'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True}

# serialize object to JSON-encoded string with schema.dumps()

dog_json = dog_schema.dumps(dog)
pprint(dog_json)
# => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'

# specify which fields to output with the only parameter, passed as a tuple.

dog_summary = DogSchema(only=("name", "breed")).dumps(dog)
pprint(dog_summary)
# => '{"name": "Snuggles", "breed": "Beagle"}'

# omit fields by passing the exclude parameter. Note the comma in the tuple.

dog_summary = DogSchema(exclude=("tail_wagging", )).dumps(dog)
pprint(dog_summary)
# => '{"name": "Snuggles", "breed": "Beagle"}'

# serialize a collection with many=True

dogs = [Dog(name="Snuggles", breed="Beagle", tail_wagging=True),
        Dog(name="Wags", breed = "Collie", tail_wagging=False)]
dictionary_list = DogSchema(many=True).dump(dogs)   # dump returns list of dictionaries
pprint(dictionary_list)
# => [{'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True},
# =>  {'breed': 'Collie', 'name': 'Wags', 'tail_wagging': False}]

json_array = DogSchema(many=True).dumps(dogs)       # dumps returns JSON-encoded list
pprint(json_array)   # NOTE: String is enclosed in parenthesis to print across multiple lines
# => ('[{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}, {"name": '
# =>  '"Wags", "breed": "Collie", "tail_wagging": false}]')
```

```py
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
```

## Resources

- [marshmallow](https://pypi.org/project/marshmallow/)
- [marshmallow quickstart](https://marshmallow.readthedocs.io/en/stable/quickstart.html)
- [pprint module](https://docs.python.org/3/library/pprint.html#module-pprint)
