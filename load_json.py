#!/usr/bin/python3

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
import json


with open('file.json', "w") as json_file:
    json.dump(storage.all(), json_file)
