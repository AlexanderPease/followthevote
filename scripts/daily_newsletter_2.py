import sys
try:
	sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
except:
	print "could not import -- must be running on heroku"

from lib import emailsdb

response3 = emailsdb.add_list_to_email()
print response3

