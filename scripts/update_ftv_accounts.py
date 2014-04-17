''' Updates FTV twitter accounts of politicians'''
import sys, os
try: 
    sys.path.insert(0, '/Users/AlexanderPease/git/ftv/followthevote')
    import settings
except:
    pass

from db import politiciandb
import twitter as python_twitter

# Using tweepy
def update_all_ftv2():
	for p in politiciandb.find_all_with_ftv():
		print "Updating %s..." % p['name']
		api = politiciandb.login_tweepy(p)

		profile_img_path = settings.get('project_root') + '/static/img/congress.jpeg'
		api.update_profile_image(profile_img_path)
		background_img_path = settings.get('project_root') + '/static/img/congress.jpeg'
		api.update_profile_background_image(background_img_path, tile='true') # Not working

def update_all_ftv():
	for p in politiciandb.find_all_with_ftv():
		print "Updating %s..." % p['name']
		api = politiciandb.login_twitter(p)
		
		# Get all twitter ids and save to database
		user = api.VerifyCredentials()
		p['ftv']['id'] = user.id
		politiciandb.save(p)

		# Set description, name, location, and url...
		if 'twitter' in p.keys():
			p['ftv']['description'] = 'Tweeting the Congressional votes of %s' % p['twitter'] # 160 char max
			if len(p['ftv']['description']) > 160:
				print len(p['ftv']['name'])
				raise Exception
		else:
			p['ftv']['description'] = 'Tweeting the Congressional votes of %s' % p['brief_name'] # 160 char max
			if len(p['ftv']['description']) > 160:
				print len(p['ftv']['name'])
				raise Exception
		
		p['ftv']['name'] = 'FTV for %s' % p['brief_name'] # 20 char max
		if len(p['ftv']['name']) > 20:
			p['ftv']['name'] = p['ftv']['name'].replace('.', '')
			if len(p['ftv']['name']) > 20:
				p['ftv']['name'] = "FTV @%s" % p['twitter_id']
				if len(p['ftv']['name']) > 20:
					print p['ftv']['name']
					print len(p['ftv']['name'])
					raise Exception

		# ...and write
		api.UpdateProfile(name=p['ftv']['name'], 
						location='Washington, D.C.', 
						description=p['ftv']['description'],
						profileURL='http://followthevote.org')
		politiciandb.save(p)

		# Set profile image and background image
		# TODO

		# Potentially change screen_name, if needed


		# Make every FTV account follow every other FTV account
		for p2 in politiciandb.find_all_with_ftv():
			if not p == p2:
				politiciandb.add_friend(p, p2)
		


''' Update @FollowTheVote '''
def update_ftv_twitter():
	api = python_twitter.Api(consumer_key=settings.get('twitter_consumer_key'),
                consumer_secret=settings.get('twitter_consumer_secret'),
                access_token_key=settings.get('ftv_twitter_consumer_key'),
                access_token_secret=settings.get('ftv_twitter_consumer_secret'))
	
	# Make @FollowTheVote followsubl . all FTV and politician accounts
	for p in politiciandb.find_all():
		if 'twitter_id' in p.keys():
			if not api.LookupFriendship(screen_name=p['twitter_id']):
				try:
					api.CreateFriendship(screen_name=p['twitter_id'])
				except:
					print "Failed to add politician's twitter: %s" % p['twitter_id']
		if 'ftv' in p.keys():
			if not api.LookupFriendship(screen_name=p['twitter_id']):
				try:
					api.CreateFriendship(screen_name=p['ftv']['twitter'])
				except:
					print "Failed to add FTV twitter: %s " % p['ftv']['twitter']

def main():
    #update_all_ftv()
    update_all_ftv2()
    #update_ftv_twitter()

if  __name__ =='__main__':main()