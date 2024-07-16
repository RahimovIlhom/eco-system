from geopy.distance import geodesic


def get_distance(location1: tuple[float, float], location2: tuple[float, float]) -> float:
    return geodesic(location1, location2).meters
