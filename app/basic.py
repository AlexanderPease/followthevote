import tornado.web
import requests
import settings
import simplejson as json
import os
import httplib
import logging

from db import userdb

class BaseHandler(tornado.web.RequestHandler):
  def __init__(self, *args, **kwargs):
    super(BaseHandler, self).__init__(*args, **kwargs)
    #user = self.get_current_user()
    #css_file = "%s/css/threatvector.css" % settings.tornado_config['static_path']
    #css_modified_time = os.path.getmtime(css_file)
      
    self.vars = {
      #'user': user,
      #'css_modified_time': css_modified_time
    }
                
  def render(self, template, **kwargs):
    # add any variables we want available to all templates
    kwargs['user_obj'] = None
    kwargs['user_obj'] = userdb.get_user_by_screen_name(self.current_user)
    kwargs['current_user_can'] = self.current_user_can 
    kwargs['settings'] = settings 
    kwargs['body_location_class'] = ""
    
    if 'msg' not in kwargs.keys():
      kwargs['msg'] = ""
    if 'err' not in kwargs.keys():
      kwargs['err'] = ""

    if self.request.path == "/":
      kwargs['body_location_class'] = "home"
  
    super(BaseHandler, self).render(template, **kwargs)
    
  def get_current_user(self):
    return self.get_secure_cookie("username")
      
    
  def is_blacklisted(self, screen_name):
    u = userdb.get_user_by_screen_name(screen_name)
    if u and 'user' in u.keys() and 'is_blacklisted' in u['user'].keys() and u['user']['is_blacklisted']:
      return True
    return False

  def current_user_can(self, capability):
    """
    Tests whether a user can do a certain thing.
    """
    result = False
    u = userdb.get_user_by_screen_name(self.current_user)
    if u and 'role' in u.keys():
      try:
        if capability in settings.get('%s_capabilities' % u['role']):
          result = True
      except:
        result = False
    return result
