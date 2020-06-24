import psycopg2
import db_config as config


class nxdb:
    '''Singleton class for database connection'''
    
    __connection = None

    def getConnection():
        if nxdb.__connection == None:
            dbconf = config.nxdown_db
            nxdb.__connection = psycopg2.connect(**dbconf)
            print("[DB connection] Connected.")
        return nxdb.__connection

    def __init__(self):
         raise Exception("Usage: nxdb.getConnection() !")