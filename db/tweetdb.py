import urllib
import json
from mongo import db
import pymongo, logging

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

''' kwarg must be a dict '''
def find_one(kwarg):
    return db.tweet.find_one(kwarg)

''' Returns politician of given bioguide_id '''
def find_by_id(t_id):
    return db.tweet.find_one({'_id':t_id})

''' Saves a tweet to the database.
    Must match entire vote dict to update vs. upsert '''
def save(t):
    return db.tweet.update({'vote':t['vote']}, t, upsert=True)

'''
def remove(intro):
  if 'id' in intro.keys():
    return db.brittbot.remove({'id':intro['id']})
'''



