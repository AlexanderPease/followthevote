import urllib
import json
from mongo import db
import pymongo, logging

"""
{
  'user': { 
    'id_str':'', 
    'auth_type': '', 
    'username': '', 
    'fullname': '', 
    'screen_name': '', 
    'profile_image_url_https': '', 
    'profile_image_url': '', 
    'is_blacklisted': False 
    },
  'access_token': { 'secret': '', 'user_id': '', 'screen_name': '', 'key': '' },
  'email_address': '',
  'role': '',
  'tags':[],
  "disqus_token_type": "Bearer",
  "disqus_access_token": "",
  "disqus_expires_in": 0,
  "disqus_refresh_token": "",
  "disqus_username": "",
  "disqus_user_id": 0,
  'yammer' {
    'access_token': {
      'token'
    }
    lots of other stuff
  }
  'in_usvnetwork': False
}

"""

###########################
### Database methods
###########################

''' Returns all politicians, unless filtered '''
def find_all(spec=None, fields=None):
	print spec
	return list(db.politician.find(spec=spec, fields=fields))

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

'''
def remove(intro):
  if 'id' in intro.keys():
    return db.brittbot.remove({'id':intro['id']})
'''

###########################
### Individual property methods
###########################

''' Politician's own twitter handle '''
def twitter(p):
  if 'twitter' in p.keys():
    return p['twitter']
  else:
    return None



