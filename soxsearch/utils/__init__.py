DIST_PER_LAT_SEC = 30.8184 #meter
DIST_PER_LNG_SEC = 25.2450 #meter
DEGREE_PER_SEC = 0.00027778


def dist2degree(distance):
    lat_seconds = round(distance / DIST_PER_LAT_SEC, 7)
    lat_degree = round(lat_seconds * DEGREE_PER_SEC, 7)

    lng_seconds = round(distance / DIST_PER_LNG_SEC, 7)
    lng_degree = round(lng_seconds * DEGREE_PER_SEC, 7)

    latlng_movement = {
        'lat': lat_degree,
        'lng': lng_degree
    }

    return latlng_movement
