import pymysql
import pymongo
import json
import re

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
    addr = str(event['address'])
    firstHalf = addr.split(' ')[0]
    firstHalf = re.sub("[^0-9]", "", firstHalf)
    street_address = addr.split(',')[0].split(' ')
    block_id = str((int(firstHalf)//100)*100) + ''.join(filter(lambda x: x.isalpha(), street_address[1:]))
    processed_address = [street_address[0] + ' ' + ' '.join(filter(lambda x: x.isalpha(), street_address[1:]))] + addr.split(',')[1:]
    processed_address = ','.join(processed_address)
    print('SELECT num_cases FROM Addresses WHERE _address = "' + str(processed_address) + '"')
    with conn.cursor() as cur:
        # finds count of all cases
        cur.execute('SELECT num_cases FROM Addresses WHERE _address = "' + str(processed_address) + '"')
        result=cur.fetchone()
        conn.commit()
    conn.commit()
    # adds number of cases at addr to response
    if result is not None:
        resp['numCases'] = result[0]

    ########## MongoDB ##########
    # gets violations document for address in mongoDB
    cur = col.find({'Address': processed_address})
    if(cur.count() > 0):
        resp['Address'] = processed_address
        for x in cur:
            resp['maskViolations'] += x['mask']
            resp['sdViolations'] += x['socialDistancing']
            resp['sickViolations'] += x['sick']
            resp['dirtyViolations'] += x['dirty']
            numComp = 3
            if len(x['violations']) < 3:
                numComp = len(x['violations'])
                print(numComp)
            for i in range(numComp):
                resp['complaints'].append(x['violations'][i])
    
    client.close()
    
    addrData = json.dumps(resp)
    addrData_loaded = json.loads(addrData)
    return addrData_loaded