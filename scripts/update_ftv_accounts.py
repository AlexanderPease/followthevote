''' Updates FTV twitter accounts of politicians'''
import sys, os
try: 
    sys.path.insert(0, '/Users/AlexanderPease/git/ftv/followthevote')
    import settings
except:
    pass

from db import politiciandb
import twitter as python_twitter

def update_all_ftv():
	
	for p in politiciandb.find_all_with_ftv():
		print "Updating %s..." % p['name']
		api = politiciandb.login_twitter(p)
		
		# Get all twitter ids and save to database
		user = api.VerifyCredentials()
		p['ftv']['id'] = user.id
		politiciandb.save(p)

		# Set name, description, image, etc.
		if 'twitter' in p.keys():
			p['ftv']['description'] = '' % p['ftv']['twitter'] # 160 char max
		
		p['ftv']['name'] = 'FTV for %s' % p['ftv']['brief_name'] # 20 char max
		if len(p['ftv']['name']) > 20:
			print len(p['ftv']['name'])
			raise Exception


		#api. ('Washington, D.C.')
		#api. ('http://followthevote.org')

		# Make every FTV account follow every other FTV account
		for p2 in politiciandb.find_all_with_ftv():
			if not p == p2:
				politiciandb.add_friend(p, p2)

	# Make @FollowTheVote follows all FTV accounts
	# TODO

	



''' Makes sure @FollowTheVote is following all FTV accounts '''
def update_ftv_twitter():
	print settings.get('twitter_consumer_key')
	print settings.get('twitter_consumer_secret')
	print settings.get('ftv_twitter_consumer_key')
	print settings.get('ftv_twitter_consumer_secret')

	api = python_twitter.Api(consumer_key=settings.get('twitter_consumer_key'),
                consumer_secret=settings.get('twitter_consumer_secret'),
                #access_token_key="2242697833-DiyEb0L6YvGo2zCApo1NSgay9Ul5DpZNOAOPyLR",
                #access_token_secret="JXtFJTvsI1KgyDggamOxUd54AHoBABoatO1x5lYytZTnH")
                access_token_key=settings.get('ftv_twitter_consumer_key'),
                access_token_secret=settings.get('ftv_twitter_access_secret'))
	print api

def main():
    update_all_ftv()
    #update_ftv_twitter()

if  __name__ =='__main__':main()