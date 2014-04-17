import settings
from mongoengine import *
import tweepy

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

	def name(self):
		return self.title + ". " + self.first_name + " " + self.last_name

	def brief_name(self):
		return self.title + ". " + self.last_name

	''' Log in using tweepy '''
	def login_twitter(self):
		try:
		    auth = tweepy.OAuthHandler(settings.get('twitter_consumer_key'), settings.get('twitter_consumer_secret'))
		    auth.set_access_token(self.ftv.access_key, self.ftv.access_secret)
		    return tweepy.API(auth)
		except:
		    if self.ftv:
		      print "@%s's account %s failed to authenticate with API" % (self.brief_name, self.ftv.twitter)
		      raise Exception
		    else: 
		      #print '@%s does not have an FTV account' % p['brief_name']
		      return None

	''' Actually tweet from their FTV account! 
	    Returns True if successfully tweeted, False if failed '''
	def tweet(self, t):
	  api = self.login_twitter()
	  if api:
	    try:
	      status = api.PostUpdate(t)
	      print '@%s posted status: %s' % (self.ftv.twitter, t)
	      return True
	    except:
	      # raise Exception
	      print '@%s FAILED to post status: %s' % (self.ftv.twitter, t)
	      return False



''' If p has FTV account, friend another twitter account '''
'''
def add_friend(p, new_friend):
  if 'ftv' not in p.keys():
    return False

  # If new_friend is a dict, not a string
  if type(new_friend) is dict:
    try:
      new_friend = new_friend['ftv']['twitter']
    except:
      raise Exception

  # Make sure not adding self
  if new_friend == p['ftv']['twitter']:
    return

  # Create friendship
  api = login_twitter(p)
  user = api.CreateFriendship(screen_name=new_friend) # user is python_twitter.user instance
  print '%s now following %s' % (p['ftv']['twitter'], new_friend)
'''


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



