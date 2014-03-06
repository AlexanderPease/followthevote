''' Updates FTV twitter accounts of politicians'''
import sys, os
try: 
    sys.path.insert(0, '/Users/AlexanderPease/git/ftv/followthevote')
    import settings
except:
    pass

from db import politiciandb


''' Makes sure @FollowTheVote is following all FTV accounts '''
def update_follow_the_vote():
	