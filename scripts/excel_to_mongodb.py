import sys, os
try: 
    sys.path.insert(0, '/Users/AlexanderPease/git/ftv/followthevote')
    import settings
except:
    print 'Could not import settings.py'

import csv
from db.mongo import db


def save(doc):
	return db.paid_twitter.update({'twitter':doc['twitter']}, doc, upsert=True)

''' Writes account info from excel into a mongodb collection '''
def excel_to_mongodb(filename):
    with open(filename, 'U') as f:
        reader = csv.reader(f, dialect=csv.excel_tab)
        for row_list in reader:
            row_string = row_list[0]
            row = row_string.split(',')
            doc = {'name': row[0],
            	'twitter': row[1],
            	'twitter_password': row[2],
            	'email': row[4],
            	'email_password': row[5]}
            save(doc)


def main():
    excel_to_mongodb('../50 Twitter Accounts_Alexander Pease.csv')

if __name__ == "__main__":
    main()
