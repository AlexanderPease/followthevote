''' Inits or updates politiciandb with Sunlight database info '''
from sunlight import congress
from db import politiciandb

politicians = congress.legislators(title='Rep')
politicians = politicians + congress.legislators(title='Sen')
print type(politicians[0])
print politicians[0]
for politician in politicians:
    '''
    p = {first_name=politician['firstname'], 
        last_name=politician['lastname'],
        state=politician['state'],
        district=politician['district'],
        party=politician['party'],
        title=politician['title'],
        portrait_id=politician['bioguide_id']

    }
    new_politician, created_flag = politiciandb.save(p)
    '''
    
    '''
    if politician['twitter_id']:
        new_politician.add_twitter(politician['twitter_id'])
    else:
        print '%s does not have twitter' % new_politician
    '''