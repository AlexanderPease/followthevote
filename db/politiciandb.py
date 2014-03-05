import urllib
import json
import settings
from mongo import db
import pymongo, logging
import twitter # bear/python-twitter

"""
{
    "_id": {
        "$oid": "530f7c5efd6e45e48ff04c3b"
    },
    "first_name": "Vance",
    "last_name": "McAllister",
    "name": "Rep. Vance McAllister",
    "district": 5,
    "title": "Rep",
    "portrait_path": "img/200x250/DEFAULT.jpg",
    "twitter_id": "RepMcAllister",
    "bioguide_id": "M001192",
    "state": "LA",
    "chamber": "House",
    "brief_name": "Rep. McAllister",
    "party": "R",
    "full_state_name": "Louisiana",
    "ftv": {
        "twitter": "FTV_LA5",
        "email": "LA5@followthevote.org",
        "password": "statueoflibertyLA5",
        "access_key": "2291790752-vKBWfp432GoRWZY47m3yXxUefMciaRstS8lrSTf",
        "access_secret": "CphtWxvKL8XwyP5KeaJOuqufanqJwNCzFyeb3Uf1z6vpm"
    }
}

"""

###########################
### Database methods
###########################

''' Returns all politicians, unless filtered '''
def find_all(spec=None, fields=None):
	return list(db.politician.find(spec=spec, fields=fields, sort=[('ftv', pymongo.DESCENDING)]))

''' kwarg must be a dict. Ex: {'twitter_id': 'SenSchumer'}'''
def find_one(kwarg):
    return db.politician.find_one(kwarg)

''' Returns politician of given bioguide_id '''
def find_by_id(p_id):
    return db.politician.find_one({'bioguide_id':p_id})

''' Saves an intro to the database. Arg is a dict.
	Can be brand new or updating existing. '''
def save(p):
	if 'bioguide_id' not in p.keys() or p['bioguide_id'] == '':
		raise Exception
	return db.politician.update({'bioguide_id':p['bioguide_id']}, p, upsert=True)

''' Return all senators '''
def senators():
  return db.politician.find({'title':'Sen'})

''' Return all representatives '''
def representatives():
  return db.politician.find({'title':'Rep'})

'''
def remove(intro):
  if 'id' in intro.keys():
    return db.brittbot.remove({'id':intro['id']})
'''

###########################
### Individual property methods
###########################
''' Actually tweet from their FTV account! 
    Returns True if successfully tweeted, False if failed '''
def tweet(p, t):
  api = login_twitter(p)
  if api:
    try:
      #status = api.PostUpdate(status)
      print '@%s posted status' % self.handle
      return True
    except:
      print '@%s FAILED to post status: %s' % (self.handle, status)
      return False

''' Log in to twitter w/ this politician's FTV account '''
def login_twitter(p):
  api = twitter.Api(consumer_key=settings.get('twitter_consumer_key'),
                consumer_secret=settings.get('twitter_consumer_secret'),
                access_token_key=p['ftv']['access_key'],
                access_token_secret=p['ftv']['access_secret'])
  try:
    print settings.get('twitter_consumer_secret')
    print p['ftv']['access_secret']
    api = twitter.Api(consumer_key=settings.get('twitter_consumer_key'),
                consumer_secret=settings.get('twitter_consumer_secret'),
                access_token_key=p['ftv']['access_key'],
                access_token_secret=p['ftv']['access_secret'])
    return api
  except:
    if 'ftv' in p.keys():
      print "@%s's account %s failed to authenticate with API" % (p['brief_name'], p['ftv']['twitter'])
      print p
      raise Exception
    else: 
      #print '@%s does not have an FTV account' % p['brief_name']
      return None

''' Politician's own twitter handle '''
def twitter(p):
  if 'twitter' in p.keys():
    return p['twitter']
  else:
    return None




