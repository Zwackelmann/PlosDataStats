from main.util.db import openDb

db = openDb("stuff/localconnect.json")
f = open("/home/simon/user_articles.txt")

for line in f:
    s = line.split(";")
    if len(s) < 2:
        raise ValueError("There was a line without any semicolon - cannot be!!")
    if len(s) == 2: # expected normal case
        usr = int(s[0])
        concept = s[1][0:255]
    else: # semicolon occurres in concept name
        usr = int(s[0])
        concept = (";".join(s[1:]).strip())[0:255]

    cursor = db.cursor()
    cursor.execute("INSERT INTO user_tweet_concepts VALUES (%s, %s)", (usr, concept))
    db.commit()