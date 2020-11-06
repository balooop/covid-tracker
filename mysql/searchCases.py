import pymysql

#rds settings
rds_host  = 'covid-tracker-locations-db.c8wmeg2eqxqu.us-east-2.rds.amazonaws.com'
username = 'admin'
password = 'password'
db_name = 'covid_locations_db'  

conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
    
def handler(event, context):
    ### find all cases matching the given address from the cases table

    # connects to database
    with conn.cursor() as cur:
        # finds count of all cases
        cur.execute('SELECT num_cases FROM Addresses WHERE _address = "' + str(event['address']) + '"')
        result=cur.fetchone()
        conn.commit()
    conn.commit()
    if result is None:
        return 0
    return result[0]
    