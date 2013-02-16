from mongoengine import *
connect('mongoengine')

class Track(EmbeddedDocument):
    id = IntField()
    pid = IntField()
    title = StringField(max_length=50)
    price = DecimalField()
    statName = StringField(max_length=50)
    statVoice = StringField(max_length=50)
    fre = StringField(max_length=50)
    freVoice =  StringField(max_length=50) 
    posName = StringField(max_length=50)
    posVoice = StringField(max_length=50)

class Customer(Document):
    name = StringField(max_length=120, required=True)
    email = EmailField()
    password_hash = StringField(max_length=120)
    Tracks = ListField(EmbeddedDocumentField(Track))