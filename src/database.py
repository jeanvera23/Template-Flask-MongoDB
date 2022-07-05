from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


class User(db.Document):
    email = db.StringField(required=True,unique=True)
    password = db.StringField(required=True)
    firstName = db.StringField()
    lastName = db.StringField()
    age = db.IntField()
    updatedAt = db.DateTimeField(default=datetime.utcnow)
    createdAt = db.DateTimeField(default=datetime.utcnow)

    def toJson(self):
        return {
            "id": str(self.pk),
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName
        }
