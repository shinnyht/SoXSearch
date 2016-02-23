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
        initial_param = True

        SQL = "select nodeID, id, type, Y(latlng), X(latlng) \
            from soxdb.nodelist "

        if lat and lng:
            initial_param = False
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
                SQL = SQL + " where nodeID regexp '^.*" + name + ".*'"
                initial_param = False
            else:
                SQL = SQL + " and nodeID regexp '^.*" + name + ".*'"

        if datatype:
            if initial_param:
                SQL = SQL + "where type='" + datatype + "'"
                initial_param = False
            else:
                SQL = SQL + " and type='" + datatype + "'"

        result = self.data_manager.fetchRecords(SQL)
        json_responce = self.createNodeListJSON(result)

        self.data_manager.CloseDBConnection()

        return json_responce


    def createNodeListJSON(self, dictdata):
        nodelist_json = {"nodelist": [], "total": 0, "time": 0}
        for row in dictdata:
            node = {
                "nodeID": row[0],
                "id": row[1],
                "datatype": row[2],
                "longitude": row[3],
                "latitude": row[4],
            }
            nodelist_json["nodelist"].append(node)

        nodelist_json["total"] = len(dictdata)

        return nodelist_json
