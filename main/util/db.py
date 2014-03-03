import MySQLdb
import json

def openDb(connFilename):
    conf = json.load(open(connFilename))
    return MySQLdb.connect(
        host=conf['host'],
        user=conf['user'],
        passwd=conf['passwd'],
        db=conf['db']
    )