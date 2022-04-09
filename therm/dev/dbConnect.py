import MySQLdb

host = "localhost"
user = "sensordev"
passwd = user
db = user

db = MySQLdb.connect(host, user, passwd, db)

cur=db.cursor()

cur.execute("""SELECT * FROM sensordev""")

print "Attempting db read..."
for row in cur.fetchall() :
    print row

rowCount = cur.execute("""SELECT COUNT(*) FROM sensordev""")
print "Finished reading " + str(rowCount-1) + " rows from " + user + " db."

cur.close()
db.close()
