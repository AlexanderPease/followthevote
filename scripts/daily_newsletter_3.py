import sys
try:
	sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
except:
	print "could not import -- must be running on heroku"

from lib import emailsdb

response4 = emailsdb.send_email()
print response4