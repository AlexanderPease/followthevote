import sys
sys.path.insert(0, '/Users/nick/dev/usv/usv.com')
import settings
import logging
from datetime import datetime, timedelta
import optparse
from lib import statsdb, postsdb

parser = optparse.OptionParser()
parser.add_option('-e', '--end',
	action="store", dest="end_date",
	help="end date", default="today")
	
options, args = parser.parse_args()

if options.end_date == "today":
	end_date = datetime.today()
	dow = datetime.today().weekday()
	offset = dow + 1
	end_date = datetime.today() - timedelta(days=offset)
	end_date_str = "%s/%s/%s" % (end_date.month, end_date.day, end_date.year)
else:
	end_date_str = options.end_date
	end_date = datetime.strptime(end_date_str, "%m-%d-%Y")

start_date = end_date - timedelta(days=7)

count = postsdb.get_post_count_for_range(start_date, end_date)
unique_posters = postsdb.get_unique_posters(start_date, end_date)
single_post_count = 0
for user in unique_posters:
	if user['count'] == 1:
		single_post_count += 1


print "Week ending %s" % end_date_str
print "+++ %s posts" % count 
print "+++ %s unique posters" % len(unique_posters)
print "+++ %s one-time posters" % single_post_count
