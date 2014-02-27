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

''' Returns all intros '''
def get_all():
	return list(db.politician.find())

''' Returns politician of given id '''
def get_by_id(p_id):
    return db.politician.find_one({'id':p_id})

''' Saves an intro to the database. Arg is a dict.
	Can be brand new or updating existing. '''
def save(p):
	if 'id' not in p.keys() or p['id'] == '':
		raise Exception
	return db.politician.update({'id':p['id']}, p, upsert=True)

'''
def remove(intro):
	if 'id' in intro.keys():
		return db.brittbot.remove({'id':intro['id']})
'''

