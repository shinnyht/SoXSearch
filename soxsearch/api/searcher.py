import re
import soxsearch.utils
from soxsearch.utils.DBManager import DBManager

class Searcher:

    def __init__(self, host, db, user, passwd, charset):
        self.data_manager = DBManager(
            host, db, user, passwd, charset
        )


    def searchByLocation(self, base_point, radius):
        # get how many degrees to move from the center point
        degrees_to_move = dist2degree(radius)

        # HERE MySQL search

        return True


    def searchByName(self, name):
        self.data_manager.EstablishDBConnection()

        # HERE MySQL search
        sql = "select nodeID, id, X(latlng), Y(latlng) \
            from nodelist where nodeID regexp \
            '^.*" + name + ".*'"
        result = self.data_manager.fetchRecords(sql)

        nodelist_json = {"nodelist": []}
        for row in result:
            node = {
                "nodeID": row[0],
                "id": row[1],
                "latitude": row[2],
                "longitude": row[3],
            }
            nodelist_json["nodelist"].append(node)

        self.data_manager.CloseDBConnection()

        return nodelist_json


    def searchByType(self, sensorType):
        self.data_manager.EstablishDBConnection()

        # HERE MySQL search
        sql = "select nodeID, id, X(latlng), Y(latlng) \
            from nodelist where type='" + sensorType + "'"
        result = self.data_manager.fetchRecords(sql)

        nodelist_json = {"nodelist": []}
        for row in result:
            node = {
                "nodeID": row[0],
                "id": row[1],
                "latitude": row[2],
                "longitude": row[3],
            }
            nodelist_json["nodelist"].append(node)

        self.data_manager.CloseDBConnection()

        return nodelist_json
