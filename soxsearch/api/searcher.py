import re
from soxsearch.utils import dist2degree
from soxsearch.utils.DBManager import DBManager

class Searcher:

    def __init__(self, host, db, user, passwd, charset):
        self.data_manager = DBManager(
            host, db, user, passwd, charset
        )


    def searchByLocation(self, latitude, longitude, radius):
        self.data_manager.EstablishDBConnection()

        # get how many degrees to move from the center point
        degrees_to_move = dist2degree(radius)
        rangecorners = {
            "lat1": latitude - degrees_to_move["lat"],
            "lng1": longitude - degrees_to_move["lng"],
            "lat2": latitude + degrees_to_move["lat"],
            "lng2": longitude + degrees_to_move["lng"]
        }

        # HERE MySQL search
        sql = "select nodeID, id, X(latlng), Y(latlng) \
            from nodelist where MBRContains(GeomFromText \
            ('LineString(" \
            + str(rangecorners["lat1"]) + " " \
            + str(rangecorners["lng1"]) + ", " \
            + str(rangecorners["lat2"]) + " " \
            + str(rangecorners["lng2"]) + ")'), latlng)"


        result = self.data_manager.fetchRecords(sql)
        json_responce = self.createNodeListJSON(result)

        self.data_manager.CloseDBConnection()

        return json_responce


    def searchByName(self, name):
        self.data_manager.EstablishDBConnection()

        # HERE MySQL search
        sql = "select nodeID, id, X(latlng), Y(latlng) \
            from nodelist where nodeID regexp \
            '^.*" + name + ".*'"
        result = self.data_manager.fetchRecords(sql)
        json_responce = self.createNodeListJSON(result)

        self.data_manager.CloseDBConnection()

        return json_responce


    def searchByType(self, sensorType):
        self.data_manager.EstablishDBConnection()

        # HERE MySQL search
        sql = "select nodeID, id, X(latlng), Y(latlng) \
            from nodelist where type='" + sensorType + "'"
        result = self.data_manager.fetchRecords(sql)
        json_responce = self.createNodeListJSON(result)

        self.data_manager.CloseDBConnection()

        return json_responce


    def createNodeListJSON(self, dictdata):
        nodelist_json = {"nodelist": []}
        for row in dictdata:
            node = {
                "nodeID": row[0],
                "id": row[1],
                "latitude": row[2],
                "longitude": row[3],
            }
            nodelist_json["nodelist"].append(node)

        return nodelist_json
