import MySQLdb
import json

conf = json.loads(open("mysqlconnect.json"))

db = MySQLdb.connect(
    host=conf['host'],
    user=conf['user'],
    passwd=conf['passwd'],
    db=conf['db']
)

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