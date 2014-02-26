import app.basic
from db import companiesdb, jobsdb, postsdb
from slugify import slugify


########################
### Homepage
########################
class Index(app.basic.BaseHandler):
  def get(self):
    self.render('base.html')