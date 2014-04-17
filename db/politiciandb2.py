import settings
from mongoengine import *

mongo_database = settings.get('mongo_database')
connect('politician', host=mongo_database['host'])

class FTV(EmbeddedDocument):
	twitter = StringField()
	twitter_id = IntField() # used to be id
	access_key = StringField()
	access_secret = StringField()
	name = StringField()
	description = StringField()

	email = StringField()
	email_password = StringField() # used to be password

class Politician(Document):
	first_name = StringField(required=True)
	last_name = StringField(required=True)
	title = StringField(required=True)
	district = IntField() # Senators don't have (but they could have Jr/Sr)
	state = StringField(required=True, max_length=2)
	party = StringField(required=True, max_length=1)
	chamber = StringField(required=True)

	portrait_path = StringField(required=True)
	twitter = StringField(required=True, max_length=16) # Politician's personal twitter
	bioguide_id = StringField()

	ftv = EmbeddedDocumentField("FTV")





'''SCRAP


    for p in politiciandb.find_all():
      p['twitter'] = p['twitter_id']
      p['twitter_id'] = ""
      #if 'ftv' in p.keys():
        #p['ftv']['email_password'] = p['ftv']['password']
        #p['ftv']['twitter_password'] = p['ftv']['password']
        #p['ftv']['twitter_id'] = p['ftv']['id']
      politiciandb.save(p)

    
    for p in politiciandb.find_all():
      p2 = politiciandb2.Politician(first_name = p['first_name'],
                              last_name = p['last_name'],
                              district = p['district'],
                              title = p['title'],
                              portrait_path = p['portrait_path'],
                              twitter = p['twitter_id'],
                              bioguide_id = p['bioguide_id'],
                              state = p['state'],
                              chamber='chamber',
                              party = p['party'],
                              full_state_name = p['full_state_name'])
      if 'ftv' in p.keys():
        politiciandb2.FTV()
        p2.ftv = p['ftv']

      p2.save()
      print p2
'''




