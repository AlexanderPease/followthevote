import app.basic
import tornado.web
import settings
import requests
from sunlight import congress, congress_deprecated
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
  #@tornado.web.authenticated
  def get(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      form = self.get_votes_form()
      msg = 'What shall we tweet about? Search the Congressional Archives'
      return self.render('admin/votes.html', form=form, msg=msg, votes=[])

  @tornado.web.authenticated
  def post(self):
    form = self.get_votes_form()

    # Sunlight API pukes on null args, so sanitize
    kwargs = {'per_page': 50}
    for k, v in form.iteritems(): #.cleaned_data.items():
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
    else:
      #vote = self.get_argument # vote = request.GET # assumes request comes from votes(request)
      reps_account_placeholder = "@[representative's account]"
      choice_placeholder = '[yes/no]'
      tweet_beginning = "%s voted %s on " % (reps_account_placeholder, choice_placeholder)
      form = TweetForm()
      return self.render('admin/tweet.html', vote=vote, tweet_beginning=tweet_beginning, form=form)

  @tornado.web.authenticated
  def post(self):
    if self.current_user not in settings.get('staff'):
      self.redirect('/')
    else:
      #vote = self.get_argument # vote = request.GET # assumes request comes from votes(request)
      reps_account_placeholder = "@[representative's account]"
      choice_placeholder = '[yes/no]'
      tweet_beginning = "%s voted %s on " % (reps_account_placeholder, choice_placeholder)
      form = TweetForm(request.POST)
      if not form.is_valid():
        err = 'Submitted invalid tweet!'
        self.render('admin/tweet.html', err='err', tweet_beginning=tweet_beginning, vote=vote, form=form)
      else: 
        # Create base tweet
        tweet_text = form.cleaned_data['text']
        tweet_template = tweet_beginning + tweet_text

        # Get votes for each politician from Sunlight
        kwargs = {'fields': 'voter_ids'}
        for k, v in request.GET.iteritems():
            if v:
                kwargs[k] = v
        individual_votes = congress.votes(**kwargs)
        if len(individual_votes) != 1:
            print 'Error finding votes'
            return
            #TODO figure out error handling or better transfer method
        individual_votes = individual_votes[0]['voter_ids'] # returns a dict with bioguide_ids for keys

        # Tweet for every applicable politician
        for twitter_ftv in Twitter_FTV.objects.all().exclude(handle="FollowTheVote"):
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

        return render_to_response('admin.html', {'msg': 'All accounts tweeted successfully!'}, 
    context_instance=RequestContext(request))
     

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

