import sqlite3
import urllib2
import json
import time

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
select handle from User
except 
select distinct handle from RatingChange
""")

handles = cursor.fetchall()

for handle in handles:
	rating_changes_array = json.loads(urllib2.urlopen("https://codeforces.com/api/user.rating?handle="+handle[0]).read())['result']
	print "obtendo rating changes de " + handle[0]
	for rc in rating_changes_array:
		cursor.execute("""
		INSERT INTO RatingChange(handle, oldRating, newRating, stamp) VALUES(?, ?, ?, ?)
		""", (handle[0], rc['oldRating'], rc['newRating'], rc['ratingUpdateTimeSeconds']))
	conn.commit()
	time.sleep(0.3)
	print "rating changes salvos"

conn.commit()
conn.close()
