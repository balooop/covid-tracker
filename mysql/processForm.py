import sys
import logging
import pymysql
from datetime import datetime
import uuid
#rds settings
rds_host  = 'covid-tracker-locations-db.c8wmeg2eqxqu.us-east-2.rds.amazonaws.com'
username = 'admin'
password = 'password'
db_name = 'covid_locations_db'

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
        addCase(str(event['address']), str(event['NetID']))


def addCase(addresses_visited, netid):
    ### insert case into Cases table
    # generate UUID for case
    
    # connects to database
    with conn.cursor() as cur:
        # compute 'block_id'
        street_address = addresses_visited.split(',')[0].split(' ')
        block_id = str((int(street_address[0])//100)*100) + ''.join(street_address[1:])


        # inserts case into Cases
        cur.execute('INSERT into Cases (address_visited, netid, timestamp, block_id) Values ("'+addresses_visited+'", "'+netid+'", CURRENT_TIMESTAMP, "'+block_id+'")')
        conn.commit()
        
    cur.close()
    return
    
def removeCase(netid):
    with conn.cursor() as cur:
        cur.execute('DELETE from Cases c WHERE c.netid = "'+netid+'"')
        conn.commit()

    cur.close()
    return
