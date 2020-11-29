import sys
import logging
import pymysql
from datetime import datetime
import uuid
import re
#rds settings
rds_host  = 'covid-tracker.c7ic0rieoltc.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'Cov1dgrap3'
db_name = 'covid-locations-tracker'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
    
# logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    if event['Delete'] == True:
        removeCase(str(event['NetID']))
    else:
        x = range(0,10)
        for i in x:
            addr = "address" + str(i)
            if (str(event[addr]) != ""):
                addCase(str(event[addr]), str(event['NetID']))


def addCase(addresses_visited, netid):
    ### insert case into Cases table
    # generate UUID for case
    
    # connects to database
    with conn.cursor() as cur:
        # compute 'block_id'
        firstHalf = addresses_visited.split(' ')[0]
        firstHalf = re.sub("[^0-9]", "", firstHalf)
        street_address = addresses_visited.split(',')[0].split(' ')
        block_id = str((int(firstHalf)//100)*100) + ''.join(filter(lambda x: x.isalpha(), street_address[1:]))
        processed_address = [street_address[0] + ' ' + ' '.join(filter(lambda x: x.isalpha(), street_address[1:]))] + addresses_visited.split(',')[1:]
        processed_address = ','.join(processed_address)



        # inserts case into Cases
        try:
            cur.execute('INSERT into Cases (address_visited, netid, timestamp, block_id) Values ("'+processed_address+'", "'+netid+'", CURRENT_TIMESTAMP, "'+block_id+'")')
            conn.commit()
        except pymysql.IntegrityError as e:
            logger.error("ERROR: Duplicate Value")
            logger.error(e)
            conn.commit()
        
    cur.close()
    return
    
def removeCase(netid):
    with conn.cursor() as cur:
        cur.execute('DELETE from Cases c WHERE c.netid = "'+netid+'"')
        conn.commit()

    cur.close()
    return
