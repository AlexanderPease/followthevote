import app.basic
import tornado.web
import settings
import requests, datetime
from sunlight import congress
from geopy import geocoders

from db import politiciandb, tweetdb, userdb, politiciandb2

###########################
### List the available admin tools
### /admin
###########################
class AdminHome(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')

    for p in politiciandb2.Politician.objects:
      pass

    import tweepy
    auth = tweepy.BasicAuthHandler('PevahouseGarcia', 'pwsk54RNJA')
    print auth

    msg = self.get_argument('msg', '')
    if msg == 'tweet_success':
      msg = 'All accounts successfully tweeted!'

    err = self.get_argument('err', '')
    if err == 'tweet_exists':
      err = 'This vote has already been tweeted en masse!'

    # Show recent tweets
    tweets = tweetdb.find_all()
    if len(tweets) > 10:
      tweets = tweets[0:9]
    
    self.render('admin/admin_home.html', tweets=tweets, msg=msg, err=err)


###########################
### Search Sunlight database of votes
### /admin/votes
###########################
class Votes(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')

    form = self.get_votes_form()
    msg = 'What shall we tweet about? Search the Congressional Archives'

    return self.render('admin/votes.html', form=form, msg=msg, votes=[])

  @tornado.web.authenticated
  def post(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')

    form = self.get_votes_form()

    # Sunlight API pukes on null args, so sanitize
    kwargs = {'per_page': 50}
    for k, v in form.iteritems():
      if v:
        kwargs[k] = v

    # Query Sunlight API
    votes = congress.votes(**kwargs)

    # Post-query logic
    if not votes:
      err = 'No search results, try again'
      return self.render('admin/votes.html', form=form, err=err)
    if len(votes) > 1:
      msg = 'Found %s results, please choose the correct one:' % len(votes)
      # TODO: returns max 50 results on first page. Give option to search further pages
    else:
      msg = 'Please confirm that this is the correct vote'
    return self.render('admin/votes.html', msg=msg, votes=votes, form=form)

  ''' Gets arguments for votes form '''
  def get_votes_form(self):
      # Form fields
      form = {}
      #form['roll_id'] = self.get_argument('roll_id', '')
      #form['number'] = self.get_argument('number', '')
      #form['year'] = self.get_argument('year', '')
      form['chamber'] = self.get_argument('chamber', '')
      return form

###########################
### Given a vote, tweet it for all accounts!
### /admin/tweet
###########################
REPS_ACCOUNT_PLACEHOLDER = "@[representative's account]" # redundant
CHOICE_PLACEHOLDER = "[yes/no]"

class Tweet(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')

    vote = self.get_vote() # vote is defined as the GET parameters passed into Tweet(), except tweet_text
    tweet_beginning = self.get_tweet_beginning()
    form = self.get_tweet_form()
    return self.render('admin/tweet.html', vote=vote, tweet_beginning=tweet_beginning, form=form)

  @tornado.web.authenticated
  def post(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    
    vote = self.get_vote()
    tweet_beginning = self.get_tweet_beginning()
    tweet_text = self.get_argument('tweet_text','')
    tweet_template = tweet_beginning + tweet_text


    # Check if rePOSTing. I did this once and it doesn't break anything
    # but fails when trying to tweet, so sets tweet document to 0 accounts tweeted
    existing_tweet = tweetdb.find_one({'vote':vote})
    if existing_tweet:
      return self.redirect('admin/?err=tweet_exists') 

    if len(tweet_text) > 110: # poorly hardcoded. calculated from get_tweet_beginning()
      err = 'Some tweets will exceed 140 characters in length!'
      return self.render('admin/tweet.html', err=err, tweet_beginning=tweet_beginning, vote=vote, form=self.get_tweet_form())

    else: 
      vote['fields'] = 'voter_ids'
      individual_votes = congress.votes(**vote)

      if len(individual_votes) != 1:
        print 'Error finding votes'
        raise Exception
          
      individual_votes = individual_votes[0]['voter_ids'] # returns a dict with bioguide_ids for keys

      # Tweet for every applicable politician. Yes, this is suboptimal
      tweeted = {}
      for p in politiciandb.find_all():
        ### IN FUTURE JUST USE THEIR OWN HANDLE. JUST DON"T WANT EXPOSURE YET
        # Hierarchy of name choosing
        if len(p['brief_name']) <= 16:
            name = p['brief_name']
        #elif p['twitter']:
        #    name = p['twitter']
        elif len(p['last_name']) <= 16:
            name = p['last_name']
        elif p['title'] == 'sen':
            name = "Senator"
        else:
            name = "Representative"

        # Find corresponding vote
        if p['bioguide_id'] in individual_votes:
          choice = individual_votes[p['bioguide_id']]
          if choice == 'Yea':
              choice = 'YES'
          elif choice == 'Nay':
              choice = 'NO'
          elif choice == 'Not Voting':
            choice = 'abstained'
            tweet_template.replace('voted ', '') # get rid of voting verb

          tweet = tweet_template.replace(REPS_ACCOUNT_PLACEHOLDER, name).replace(CHOICE_PLACEHOLDER, choice)
          success = politiciandb.tweet(p, tweet)
          # If successfull tweeted, save for entry to database
          if success:
            tweeted[p['bioguide_id']] = choice
      
      # Save to database
      save_tweet = {
        'datetime': datetime.datetime.now(),
        'vote': vote, 
        'tweeted': tweeted, # Who actually had FTV accounts, i.e. actually tweeted 
        'tweet_template': tweet_template,
        'placeholders': {'reps_account_placeholder': REPS_ACCOUNT_PLACEHOLDER, 'choice_placeholder': CHOICE_PLACEHOLDER},
        'tweet': tweet, # A sample tweet (always from last rep in database to tweet)
        'individual_votes': individual_votes,
        'admin': self.current_user
        }
      tweetdb.save(save_tweet)

      # Email admins
      subject = '%s tweeted!' % self.current_user
      text_body = tweet_template
      for sn in settings.get('staff'):
        admin = userdb.get_user_by_screen_name(sn)
        try:
          self.send_email(admin['email_address'], subject, text_body)
        except:
          print 'Failed to send email to admin %s' % admin['user']['username']
          pass

      return self.redirect('admin/?msg=tweet_success') 


  ''' Vote is defined as all arguments except tweet_text '''
  def get_vote(self):
    vote = self.get_all_arguments()
    # When POSTED, the parameters include tweet_text
    if 'tweet_text' in vote.keys():
      del vote['tweet_text']
    return vote

  ''' Gets arguments for votes form '''
  def get_tweet_form(self):
      return {'tweet_text': self.get_argument('tweet_text', '')}

  ''' Get placeholder  '''
  def get_tweet_beginning(self):
    return "%s voted %s on " % (REPS_ACCOUNT_PLACEHOLDER, CHOICE_PLACEHOLDER)
     

###########################
### ASCII view of database
### /admin/database
###########################
class Database(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      politicians = politiciandb.find_all()
      return self.render('admin/database.html', politicians=politicians)

