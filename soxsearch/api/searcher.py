import re
from soxsearch.utils import dist2degree
from soxsearch.utils.DBManager import DBManager

class Searcher:

    def __init__(self, host, db, user, passwd, charset):
        self.data_manager = DBManager(
            host, db, user, passwd, charset
        )


    def searchNodes(self, name, datatype, lat, lng, rad):
        self.data_manager.EstablishDBConnection()
        initial_param = False

        SQL = "select nodeID, id, type, Y(latlng), X(latlng) \
            from soxdb.nodelist "

        if lat and lng and rad:
            initial_param = True
            degrees_to_move = dist2degree(rad)
            rangecorners = {
                "lat1": lat - degrees_to_move["lat"],
                "lng1": lng - degrees_to_move["lng"],
                "lat2": lat + degrees_to_move["lat"],
                "lng2": lng + degrees_to_move["lng"]
            }

            SQL = SQL + "where MBRContains(GeomFromText \
                ('LineString(" \
                + str(rangecorners["lat1"]) + " " \
                + str(rangecorners["lng1"]) + ", " \
                + str(rangecorners["lat2"]) + " " \
                + str(rangecorners["lng2"]) + ")'), latlng)"
        if name:
            if initial_param:
                SQL = SQL + " and nodeID regexp '^.*" + name + ".*'"
            else:
                SQL = SQL + " where nodeID regexp '^.*" + name + ".*'"
                initial_param = True

        if datatype:
            if initial_param:
                SQL = SQL + " and type='" + datatype + "'"
            else:
                SQL = SQL + "where type='" + datatype + "'"

        result = self.data_manager.fetchRecords(SQL)
        json_responce = self.createNodeListJSON(result)

        self.data_manager.CloseDBConnection()

        return json_responce


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
        sql = "select nodeID, id, type, Y(latlng), X(latlng) \
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
        sql = "select nodeID, id, type, Y(latlng), X(latlng) \
            from nodelist where nodeID regexp \
            '^.*" + name + ".*'"
        result = self.data_manager.fetchRecords(sql)
        json_responce = self.createNodeListJSON(result)

        self.data_manager.CloseDBConnection()

        return json_responce


    def searchByType(self, sensorType):
        self.data_manager.EstablishDBConnection()

        # HERE MySQL search
        sql = "select nodeID, id, type, Y(latlng), X(latlng) \
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
                "datatype": row[2],
                "longitude": row[3],
                "latitude": row[4],
            }
            nodelist_json["nodelist"].append(node)

        return nodelist_json
