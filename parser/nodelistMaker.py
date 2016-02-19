import sys
from extractor import Extractor
from DBManager import DBManager

reload(sys)
sys.setdefaultencoding('utf-8')


class NodeListMaker:

    def __init__(self, host, db, user, passwd, charset):
        self.data_extractor = Extractor()
        self.data_manager = DBManager(
            host, db, user, passwd, charset
        )

    def assortData(self):
        self.data_manager.EstablishDBConnection()

        # fetch all records from ofPubsubItem table
        all_data = self.data_manager.fetchRecords(
            "select serviceID,nodeID,id,payload \
            from ofPubsubItem;"
        )

        # assort records in table
        for data in all_data:
            nodeID = data[1].encode("utf-8")

            # execute when record was metadata record
            if nodeID.rfind("_meta") > -1:
                self.insertNodeListMetaDB(data)
            # execute when record was data record
            elif nodeID.rfind("_data") > -1:
                self.insertNodeListDataDB(data)

        self.data_manager.CloseDBConnection()


    def junctionDB(self):
        self.data_manager.EstablishDBConnection()

        # fetch all records from nodelist_data table
        all_data = self.data_manager.fetchRecords(
            "select serviceID,nodeID,id,X(latlng),Y(latlng) \
            from nodelist_data;"
        )

        meta_data = None
        try:
            for data in all_data:
                nodeID = data[1].encode("utf-8")

                # fetch record with certain nodeID
                meta_data = self.data_manager.fetchSingleRecords(
                    "select type from nodelist_meta \
                    where nodeID='" + nodeID + "';"
                )
                # set datatype if exists
                if meta_data:
                    datatype = meta_data[0]
                # set datatype "other" if none exists
                else:
                    datatype = "other"

                # insert new record into nodelist table
                self.insertNodeListDB(data, datatype)

            self.data_manager.CloseDBConnection()
        except Exception as e:
            print e


    def insertNodeListDB(self, data, datatype):
        serviceID = data[0]
        nodeID = data[1].encode("utf-8")
        ID = data[2]
        location = {
            "lat": data[3],
            "lng": data[4]
        }

        # generate SQL statement for nodelist table
        sql = self.data_manager.generateSQLStatement(
            "nodelist",
            serviceID,
            nodeID,
            ID,
            datatype,
            location
        )
        self.data_manager.executeSQL(sql)


    def insertNodeListMetaDB(self, data):
        serviceID = data[0]
        nodeID = data[1].encode("utf-8").replace("_meta", "")
        ID = data[2]
        payload = self.fixPayload(data[3].encode("utf-8"))

        # extract datatype from given payload
        datatype = self.data_extractor.extractDataType(payload)

        # generate SQL statement for nodelist_meta table
        sql = self.data_manager.generateSQLStatement(
            "nodelist_meta",
            serviceID,
            nodeID,
            ID,
            datatype,
            None
        )
        self.data_manager.executeSQL(sql)

    def insertNodeListDataDB(self, data):
        serviceID = data[0]
        nodeID = data[1].encode("utf-8").replace("_data", "")
        ID = data[2]
        payload = self.fixPayload(data[3].encode("utf-8"))

        # extract location from given payload
        location = self.data_extractor.extractData(payload)

        # generate SQL statement for nodelist_data table
        sql = self.data_manager.generateSQLStatement(
            "nodelist_data",
            serviceID,
            nodeID,
            ID,
            None,
            location
        )
        self.data_manager.executeSQL(sql)


    # sometimes payload is not correctly formatted
    def fixPayload(self, payload):
        fixed_payload = payload

        try:
            # fix the wrong format in payload
            tmp_payload = payload.replace(">&lt;", "><")
            fixed_payload = tmp_payload.replace("/&gt;", "/>")
        except:
            print "Payload parse error"

        return fixed_payload


if __name__ == "__main__":
    nodelistMaker = NodeListMaker(
        "hostname", # set hostname
        "db",       # set database
        "username", # set MySQL username
        "passwd",   # set password
        "utf8"
    )

    nodelistMaker.assortData()
    nodelistMaker.junctionDB()
