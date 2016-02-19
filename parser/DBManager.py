import MySQLdb

class DBManager:

    def __init__(self, host, db, user, passwd, charset):
        self.host = host
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.connector = None
        self.cursor = None


    def EstablishDBConnection(self):
        self.connector = MySQLdb.connect(
            host=self.host,
            db=self.db,
            user=self.user,
            passwd=self.passwd,
            charset=self.charset
        )
        self.cursor = self.connector.cursor()


    def CloseDBConnection(self):
        self.cursor.close()
        self.connector.close()


    def getCursor(self):
        return self.cursor


    def executeSQL(self, sql):
        try:
            self.cursor.execute(sql);
            self.connector.commit()
        except Exception as e:
            print "SQL EXECUTION ERROR"
            print str(e)


    def fetchRecords(self, sql):
        try:
            self.cursor.execute(sql);
            result = self.cursor.fetchall()

            return result
        except Exception as e:
            print "COULD NOT FETCH RECORDS"
            print str(e)
            return False


    def fetchSingleRecords(self, sql):
        try:
            self.cursor.execute(sql);
            result = self.cursor.fetchone()

            return result
        except Exception as e:
            print "COULD NOT FETCH SINGLE RECORDS"
            print str(e)
            return False


    # dirty if statements
    def generateSQLStatement(self, table, serviceID, nodeID, ID, datatype, latlng):
        sql = None

        # sql generator for nodelist_data table
        if table == "nodelist_data":
            if latlng:
                sql = "insert into " + table +  " values('" \
                    + serviceID + "', '" \
                    + nodeID + "', '" \
                    + ID + "', GeomFromText('POINT(" \
                    + latlng["lat"] + " " + latlng["lng"] + ")'));"
            else:
                sql = "insert into " + table +  " values('" \
                    + serviceID + "', '" \
                    + nodeID + "', '" \
                    + ID + "', null);"
        # sql generator for nodelist_meta table
        elif table == "nodelist_meta":
            sql = "insert into " + table +  " values('" \
                + serviceID + "', '" \
                + nodeID + "', '" \
                + ID + "', '" \
                + datatype + "');"
        # sql generator for nodelist table
        elif table == "nodelist":
            if latlng["lat"] and latlng["lng"]:
                sql = "insert into " + table +  " values('" \
                    + serviceID + "', '" \
                    + nodeID + "', '" \
                    + ID + "', '" \
                    + datatype + "', GeomFromText('POINT(" \
                    + str(latlng["lat"]) + " " \
                    + str(latlng["lng"]) + ")'));"
            else:
                sql = "insert into " + table +  " values('" \
                    + serviceID + "', '" \
                    + nodeID + "', '" \
                    + ID + "', '" \
                    + datatype + "', null);"

        return sql
