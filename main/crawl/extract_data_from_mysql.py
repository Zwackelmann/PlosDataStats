<<<<<<< HEAD
import MySQLdb
import json

db = MySQLdb.connect(
    host="130.75.152.82",
    user="saschi",
    passwd="123los",
    db="saschaexperts"
)
=======
from main.util.db import openDb

db = openDb("stuff/localconnect.json")
>>>>>>> c1d847f9933d66a47795fd212c3631dbcb27ee29

cur = db.cursor() 
cur.execute("SELECT * FROM users_twitter")

f = open("twitterUsers.json", "w")

for row in cur.fetchall():
    idusersTwitter = row[0]
    twitterScreenname = row[1]
    twitterId = row[2] if row[2] != -1 else None
    followersCount = row[3]
    statusesCount = row[4]
    friendsCount = row[5]
    accountCreatedAt = row[6]
    verifiedAccount = row[7]
    listedCount = row[8]
    description = row[9]
    location = row[10]
    name = row[11]
    favouritiesCount = row[12]

    f.write(json.dumps([twitterId, twitterScreenname, name, followersCount, statusesCount, friendsCount, listedCount]) + "\n")

f.close()