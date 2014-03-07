''' Updates FTV twitter accounts of politicians'''
import sys, os
try: 
    sys.path.insert(0, '/Users/AlexanderPease/git/ftv/followthevote')
    import settings
except:
    pass

from db import politiciandb
import twitter as python_twitter


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
    update_ftv_twitter()

if  __name__ =='__main__':main()