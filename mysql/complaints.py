from pymongo import MongoClient

username = 'user'
password = 'cs411project'
dbname = 'complaints'
client = MongoClient("mongodb+srv://user:" + password + "@cluster0.2xbcj.mongodb.net/" + dbname + "?retryWrites=true&w=majority")
db = client.test

def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }