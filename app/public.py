import app.basic
#from db import companiesdb, jobsdb, postsdb


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
        
        districts = congress_deprecated.districts_for_lat_lon(lat, lon)
        if len(districts) != 1: 
            pprint('Multiple districts for single geopoint?!') #debug
            raise Exception
        else:
            district = districts[0]

    # ZIP code method
    else:
        districts = congress_deprecated.districts_for_zip(zip_code)
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
    #representative = Politician.objects.get(title='Rep', state=district['state'], district=district['number'])
    #senators = Politician.objects.filter(title='Sen', state=district['state'])
    #legislators = {'representative': representative, 'senator1':senators[0], 'senator2':senators[1]}
    #return render_to_response('results.html', {'results': legislators}, context_instance=RequestContext(request))
    return self.render('public/results.html')