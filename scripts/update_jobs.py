# Run by Heroku scheduler every night
# If running locally, uncomment below imports
import sys
try: 
	sys.path.insert(0, '/Users/AlexanderPease/git/usv/website/usv')
except:
	pass

from lib import jobsdb

INDEED_COUNTRIES = ['US',
					'GB', # Great Britain
					'CA',
					'DE',
					'IL', # Israel
					'FR',
					'NL', # Netherlands
					'SE', # Sweden
					'IE'] # Ireland

print 'Starting update_jobs.py...'
for country in INDEED_COUNTRIES:
	jobsdb.update_country(country)
print 'Successfully updated jobs in all countries'
