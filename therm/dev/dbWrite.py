import os
import glob
import time
import MySQLdb
import datetime

host = "localhost"
user = "sensordev"
passwd = user
db = user

db = MySQLdb.connect(host, user, passwd, db)

cur=db.cursor()

while True:
    print "Trying row write..."
    tdate=str(datetime.datetime.now().date())
    ttime=str(datetime.datetime.now().time())
    temp=int(75.5366)
    print tdate
    print ttime
    print temp

    try:
        query = "INSERT INTO sensordev VALUES (%s,%s,%s)"
        args = (tdate,ttime,temp)
        cur.execute(query, args)
        db.commit()
        print "Row written."
        time.sleep(1)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        db.rollback()
        print "Row write failed."
        cur.close()
        db.close()
	time.sleep(1)
