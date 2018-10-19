import sqlite3
import urllib2
import json
import time

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

while True:
	try:
		cursor.execute("""
		select handle from User
		except 
		select distinct handle from ACSubmission
		""")
		handles = cursor.fetchall()

		for handle in handles:
			print "pegando submissoes de " + handle[0]
			submissions = json.loads(urllib2.urlopen("http://codeforces.com/api/user.status?handle=" + handle[0]).read())['result']
			tuple_list = [(handle[0], 'DELETAR', 'DELETAR')]
			for sub in submissions:
				if 'verdict' in sub.keys() and sub['verdict'] == 'OK' and len(sub['author']['members']) == 1 and 'contestId' in sub['problem'].keys():
					tuple_list.append((sub['author']['members'][0]['handle'], str(sub['problem']['contestId']) + sub['problem']['index'], sub['creationTimeSeconds']))
	
			cursor.executemany("""
			INSERT INTO ACSubmission(handle, problemIndex, stamp) VALUES(?, ?, ?)
			""", tuple_list)
			conn.commit()
			time.sleep(0.3)
			print "submissoes salvas"
	except (urllib2.HTTPError, urllib2.URLError):
		print "erro, tentando de novo"
		pass
		

conn.close()
