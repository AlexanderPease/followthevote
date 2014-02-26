# Run by Heroku Scheduler every 10min
import sys
try:
	sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
except:
	print "could not import -- must be running on heroku"
from lib import postsdb
from datetime import datetime, timedelta

postsdb.sort_posts(datetime.today())
postsdb.sort_posts(datetime.today() - timedelta(days=1))
postsdb.sort_posts(datetime.today() - timedelta(days=2))
