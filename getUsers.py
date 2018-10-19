import sqlite3
import urllib2
import json

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print "baixando dados de todos os usuarios..."
json_obj = json.loads(urllib2.urlopen("https://codeforces.com/api/user.ratedList").read())
i = 0
for usr in json_obj['result']:
	print("salvando dados do usuario " + usr['handle'])
	cursor.execute("""
	INSERT INTO User(handle) VALUES(?)
	""", (usr['handle'],))
	if 'city' in usr.keys():
		cursor.execute("""
		UPDATE User
		SET city = ? 
		WHERE handle = ?
		""", (usr['city'], usr['handle']))
	
	if 'organization' in usr.keys():
		cursor.execute("""
		UPDATE User
		SET organization = ? 
		WHERE handle = ?
		""", (usr['organization'], usr['handle']))
		
	if 'country' in usr.keys():
		cursor.execute("""
		UPDATE User
		SET country = ? 
		WHERE handle = ?
		""", (usr['country'], usr['handle']))

conn.commit()
conn.close()
