import app.basic
from db import politiciandb
from sunlight import congress 
import re
import ui_methods 


########################
### Homepage
########################
class Index(app.basic.BaseHandler):
  def get(self):
    zip_code = self.get_argument('zip_code', '')
    address = self.get_argument('address', '')

    # If no zip code or address argument, then return the basic homepage
    if not zip_code and not address:
        return self.render('public/index.html', err='', msg='')

    # Address takes precedence over ZIP code for finding legislators
    # User is only asked for address if ZIP code contains multiple districts
    if address:
        #district = district_for_address(address, request)    
        g = geocoders.GoogleV3()
        place, (lat, lon) = g.geocode(address)
        pprint(place) #support multiple locations
        try:
            place, (lat, lon) = g.geocode(address)
            pprint(place) #support multiple locations
        except: 
             return self.render('public/index.html', err='bad_address', msg='')
        
        districts = congress.locate_districts_by_lat_lon(lat, lon)
        if len(districts) != 1: 
            pprint('Multiple districts for single geopoint?!') #debug
            raise Exception
        else:
            district = districts[0]

    # ZIP code method
    else:
        districts = congress.locate_districts_by_zip(zip_code)
        # Test if zip_code is valid
        regex = re.compile('\d{5,5}')
        if not (regex.match(zip_code) and districts):
            return self.render('public/index.html', err='zip_code', msg=zip_code)
        
        # Test for single congressional district
        if len(districts) > 1:
            pprint(str(len(districts)) + ' DISTRICTS IN ZIP CODE') #debug
            return self.render('public/index.html', err='multiple_districts', msg=zip_code)
        else: 
            district = districts[0]
        
    # Get representatives and pass to results.html
    representative = politiciandb.find_one({'title': 'Rep', 'state': district['state'], 'district': district['district']})
    senators = politiciandb.find_all({'title': 'Sen', 'state': district['state']})
    print senators
    if len(senators) != 2:
        raise Exception
    return self.render('public/results.html', results=[representative, senators[0], senators[1]], ordinal=ui_methods.ordinal)