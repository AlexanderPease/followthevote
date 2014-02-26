import sys
try:
	sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
except:
	print "could not import -- must be running on heroku"
from datetime import datetime
from lib import postsdb, emailsdb


posts = postsdb.get_hot_posts_by_day(datetime.today())
slugs = []
for i, post in enumerate(posts):
  if i < 5:
    slugs.append(post['slug'])
response1 = emailsdb.construct_daily_email(slugs)
print response1
  
response2 = emailsdb.setup_email_list()
print response2