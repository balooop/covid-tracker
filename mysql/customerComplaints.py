import sys
import logging
from pymongo import MongoClient
import dns

username = 'user'
password = 'cs411project'
dbname = 'Complaints'
client = MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.2xbcj.mongodb.net/" + dbname + "?retryWrites=true&w=majority")
db = client.Complaints
    
    # we need to update the mongo based on the above here
    # need to update the number of each type of complaint for the given address
    # one entry per address in the table and you just add on the given complaints to the tuple as well as update the count for each type of complaint 
def handler(event, context):
#     var updateOutput = db.updateMany({$or: [{country: "Mexico"}, {release_year: {$gt: 2008}}]},
#                                         {$set: {country: "Australia"}});
# db.Movies.find({country:"Australia"},{_id:0, movie_name: 1, release_year:1})
    
    with db.cursor() as cur:
        cur.execute("db.insert({'blah':'b', 'eshan':'gay'})")
        conn.commit()
    conn.commit()

    maskFlag = 0
    socialDistancingFlag = 0
    sickFlag = 0
    dirtyFlag = 0
    
    maskWords = ['not wearing', 'covering', 'wearing', 'not wearing']
    socialDistancing = ['too many people', 'no social distancing']
    sick = ['cough', 'coughing', 'sick', 'ill']
    dirty = ['dirty', 'nasty', 'gross', 'not clean', '']
    
    words = event['Complaints']
    for word in maskWords:
        if word in words:
            maskFlag = 1
            break
    for word in socialDistancing:
        if word in words:
            socialDistancingFlag = 1
            break
    for word in sickFlag:
        if word in words:
            sickFlag = 1
            break
    for word in dirtyFlag:
        if word in words:
            dirtyFlag = 1
            break
    
            

