
''' Updates FTV twitter accounts of politicians'''
import sys, os
try: 
    sys.path.insert(0, '/Users/AlexanderPease/git/ftv/followthevote')
    import settings
except:
    pass

from db.politiciandb2 import Politician
import splinter

''' Updates all FTV account usernames '''
def update_usernames():
	fail_list = [] # Those accounts that failed to update
	for p in Politician.objects():
		# Calc new username
		if p.title == 'Sen':
			new_username = 'FTV_' + p.state + 'Sen' + p.seniority
		elif p.title == 'Rep':
			new_username = 'FTV_' + p.state + p.district
		else:
			if len(p.full_state_name) <= 11:
				new_username = 'FTV_' + p.full_state_name 
			else:
				new_username = 'FTV_' + p.state

		# Run splinter log in only if username needs updating
		if new_username != p.ftv.twitter:
			with splinter.Browser('chrome') as browser: # browser closes at end
		        browser.visit('https://twitter.com')

		        # Log in 
		        browser.fill('signin-email', p.ftv.twitter)
		        browser.fill('signin-password', p.ftv.twitter_password)
		        browser.find_by_type('submit').first.click()
		        
		        # After click through, read pin_code
		        #pincode = browser.find_by_css('code').first.html
			

''' Updates all FTV twitter account emails incl. verifying in Gmail'''
def update_emails():
	pass


def main():
    update_usernames()

if  __name__ =='__main__':main()

