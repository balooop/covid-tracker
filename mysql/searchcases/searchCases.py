import pymysql
import pymongo
import json

#rds settings
rds_host  = 'covid-tracker.c7ic0rieoltc.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'Cov1dgrap3'
db_name = 'covid-locations-tracker'
conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)

#mongoDB connection
client = pymongo.MongoClient("mongodb+srv://user:cs411project@cluster0.2xbcj.mongodb.net/?retryWrites=true&w=majority")
db = client[ "Complaints" ]
col = db[ "Complaints" ] 

def handler(event, context):
    ########## SQL ##########
    ### find all cases matching the given address from the cases table
    resp = {'numCases':0, 'maskViolations':0, 'sdViolations':0, 'sickViolations':0, 'dirtyViolations':0, 'complaints':[]}
    # connects to database
    with conn.cursor() as cur:
        # finds count of all cases
        cur.execute('SELECT num_cases FROM Addresses WHERE _address = "' + str(event['address']) + '"')
        result=cur.fetchone()
        conn.commit()
    conn.commit()
    # adds number of cases at addr to response
    if result is not None:
        resp['numCases'] = result[0]

    ########## MongoDB ##########
    # gets violations document for address in mongoDB
    cur = col.find({'Address': event['address']})
    if(cur.count() > 0):
        for x in cur:
            resp['maskViolations'] += x['mask']
            resp['sdViolations'] += x['socialDistancing']
            resp['sickViolations'] += x['sick']
            resp['dirtyViolations'] += x['dirty']
            for i in range(3):
                resp['complaints'].append(x['violations'][i])
    
    client.close()
    
    addrData = json.dumps(resp)
    addrData_loaded = json.loads(addrData)
    return addrData_loaded