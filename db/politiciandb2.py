import settings
from mongoengine import *

mongo_database = settings.get('mongo_database')
connect('politician', host=mongo_database['host'])

class Politician(Document):
	first_name = StringField(required=True)
	last_name = StringField(required=True)
	title = StringField(required=True)
	district = IntField(required=True)
	party = StringField(required=True, max_length=2)

	FTV is an embedded document!

