import app.basic
import tornado.web
import settings
import requests
from sunlight import congress
from geopy import geocoders

from db import politiciandb


###########################
### List the available admin tools
### /admin
###########################
class AdminHome(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      self.render('admin/admin_home.html')


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
      return self.render('admin/votes.html', form=form, err='err')
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
      form['roll_id'] = self.get_argument('roll_id', '')
      form['number'] = self.get_argument('number', '')
      form['year'] = self.get_argument('year', '')
      form['chamber'] = self.get_argument('chamber', '')
      return form

###########################
### Given a vote, tweet it for all accounts!
### /admin/tweet
###########################
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


    if len(tweet_text) > 110: # poorly hardcoded. calculated from get_tweet_beginning()
      err = 'Some tweets will exceed 140 characters in length!'
      return self.render('admin/tweet.html', err='err', tweet_beginning=tweet_beginning, vote=vote, form=self.get_tweet_form())

    else: 
      tweet_template = tweet_beginning + tweet_text
      vote['fields'] = 'voter_ids'
      individual_votes = congress.votes(**vote)
      print individual_votes

      if len(individual_votes) != 1:
          print 'Error finding votes'
          return
          #TODO figure out error handling or better transfer method
      individual_votes = individual_votes[0]['voter_ids'] # returns a dict with bioguide_ids for keys

      # Tweet for every applicable politician
      ### IN FUTURE JUST USE THEIR OWN HANDLE
      for twitter_ftv in ftv_politiciandb.get_all():
          p = twitter_ftv.politician
          # Hierarchy of name choosing
          if len(p.brief_name()) <= 16:
              name = p.brief_name()
          elif p.twitter:
              name = twitter
          elif len(p.last_name) <= 16:
              name = p.last_name
          elif p.title == 'sen':
              name = "Senator"
          else:
              name = "Representative"

          # Find corresponding vote
          if p.bioguide_id in individual_votes:
              choice = individual_votes[p.bioguide_id]
              if choice == 'Yea':
                  choice = 'YES'
              elif choice == 'Nay':
                  choice == 'NO'
              tweet = tweet_template.replace(reps_account_placeholder, name).replace(choice_placeholder, choice)
              twitter_ftv.tweet(tweet)

      return self.render('admin.html', msg='All accounts tweeted successfully!') 


  ''' Vote is defined as all arguments except tweet_text '''
  def get_vote(self):
    vote = self.get_all_arguments()
    del vote['tweet_text']
    return vote

  ''' Gets arguments for votes form '''
  def get_tweet_form(self):
      return {'tweet_text': self.get_argument('tweet_text', '')}

  ''' Get placeholder  '''
  def get_tweet_beginning(self):
    reps_account_placeholder = "@[representative's account]"
    choice_placeholder = '[yes/no]'
    return "%s voted %s on " % (reps_account_placeholder, choice_placeholder)
     

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

