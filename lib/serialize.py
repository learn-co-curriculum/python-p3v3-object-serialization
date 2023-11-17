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