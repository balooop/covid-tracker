import pymysql
import pymongo
import json
import re

#hidden DB credentials
#rds settings
rds_host  = ''
username = ''
password = ''
db_name = ''
conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)

#mongoDB connection
client = pymongo.MongoClient("")
db = client[ "" ]
col = db[ "" ] 

def handler(event, context):
    ########## SQL ##########
    ### find all cases matching the given address from the cases table
    resp = {'numCases':0, 'maskViolations':0, 'sdViolations':0, 'sickViolations':0, 'dirtyViolations':0, 'complaints':[]}
    # connects to database
    addr = str(event['address'])
    firstHalf = addr.split(' ')[0]
    firstHalf = re.sub("[^0-9]", "", firstHalf)
    street_address = addr.split(',')[0].split(' ')
    block_id = str((int(firstHalf)//100)*100) + ''.join(filter(lambda x: ('#' not in x and 'suite' not in x.lower() and 'ste' not in x.lower()), street_address[1:]))
    processed_address = [street_address[0] + ' ' + ' '.join(filter(lambda x: ('#' not in x and 'suite' not in x.lower() and 'ste' not in x.lower()), street_address[1:]))] + addr.split(',')[1:]
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
    resp['Address'] = processed_address

    ########## MongoDB ##########
    # gets violations document for address in mongoDB
    cur = col.find({'Address': processed_address})
    if(cur.count() > 0):
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
