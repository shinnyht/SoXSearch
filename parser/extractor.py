from xml.etree.ElementTree import *
import xmltodict


class Extractor:

    def __init__(self):
        pass


    def extractData(self, payload):
        # extract data form payload (currently only location)
        dictdata = xmltodict.parse(payload)
        location = self.extractLocation(dictdata)

        return location


    def extractDataType(self, payload):
        # extract datatype from payload
        dictdata = xmltodict.parse(payload)
        metadata = dictdata["device"]

        if metadata.has_key("@type"):
            return metadata["@type"]
        else:
            # return "other" as datatype if nothing exists
            return "other"


    def extractLocation(self, dictdata):
        # extract location data form payload
        transducers = None
        location = {}
        try:
            if dictdata.has_key("data"):
                transducers = dictdata["data"]["transducerValue"]

            if isinstance(transducers, list):
                for transducer in transducers:
                    if transducer["@id"] == "latitude":
                        location["lat"] = transducer["@typedValue"]
                    elif transducer["@id"] == "longitude":
                        location["lng"] = transducer["@typedValue"]

                # check if both latitude & longitude exists
                if set(("lat", "lng")) <= set(location):
                    return location
            else:
                transducer = transducers["@typedValue"]
                if transducer.find("lat") > -1:
                    location = self.getLocationFromText(transducer)

                    return location

            # return None if location info was not returned
            return None
        except Exception as e:
            print "LOCATION_ERROR"
            print str(e)
            return None


    # sometimes location is embedded in text with other data
    def getLocationFromText(self, typedValue):
        valueList = typedValue.split("&")

        location = {}
        for value in valueList:
            if value.find("lat") > -1:
                location["lat"] = value.replace("lat=", "")
            elif value.find("lon") > -1:
                location["lng"] = value.replace("lon=", "")

        return location
