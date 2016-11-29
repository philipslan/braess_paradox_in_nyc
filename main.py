import pickle, googlemaps, time, string, json, os, math
from pprint import pprint
from datetime import datetime

class TrafficEntry:
    def __init__(self, dataEntry):
        self.metaSid = dataEntry[0]
        self.metaID = dataEntry[1]
        self.metaPosition = dataEntry[2]
        self.metaCreatedTime = dataEntry[3]
        self.metaCreated = dataEntry[4]
        self.metaUpdatedTime = dataEntry[5]
        self.metaUpdated = dataEntry[6]
        self.meta = dataEntry[7]
        self.ID = float(dataEntry[8])
        self.segmentID = float(dataEntry[9])
        self.roadName = dataEntry[10]
        self.fromSt = dataEntry[11]
        self.toSt = dataEntry[12]
        self.direction = dataEntry[13]
        self.date = datetime.strptime(string.rstrip(dataEntry[14], "T00:00:00"), "%Y-%m-%d")
        self.traffic = []
        self.lat = None
        self.long = None
        for i in range(15, 39):
            self.traffic.append(float(dataEntry[i]))

class ZeroDay:
    def __init__(self, entry):
        self.day = entry


def save(dObj, sFilename):
  """Given an object and a file name, write the object to the file using pickle."""
  f = open(sFilename, "w")
  p = pickle.Pickler(f)
  p.dump(dObj)
  f.close()

def load(sFilename):
  """Given a file name, load and return the object stored in the file."""
  f = open(sFilename, "r")
  u = pickle.Unpickler(f)
  dObj = u.load()
  f.close()
  return dObj

def getAndCleanData():
    rawData = open('nyc_street_data.json')
    data = json.load(rawData)
    # Find all entries that have 0 traffic at some point in the day
    traffic_data = [TrafficEntry(entry) for entry in data]
    zeroEntries = [entry for entry in traffic_data if 0.0 in entry.traffic]
    zeroDates = set(entry.date for entry in zeroEntries)
    # instantiated google maps key
    key = os.environ['NEW_GMAPS_KEY']
    gmaps = googlemaps.Client(key=key)
    # get all streets for each zero date
    zeroDatesToStreets = {date : set() for date in zeroDates}
    streetData = {}
    count = 0
    for entry in traffic_data:
        if entry.date in zeroDatesToStreets:
            zeroDatesToStreets[entry.date].add(entry)
            from_st_string = entry.roadName + " and " + entry.fromSt + " NY"
            to_st_string = entry.roadName + " and " + entry.toSt + " NY"
            intersection_string = from_st_string + " " + to_st_string
            if intersection_string not in streetData:
                if (count%50 == 0) and count != 0:
                    print "sleeping"
                    time.sleep(1)
                    print "slept"
                from_st_loc = gmaps.geocode(from_st_string)
                to_st_loc = gmaps.geocode(to_st_string)
                count += 2
                loc1 = from_st_loc[0]['geometry']['location']
                loc2 = to_st_loc[0]['geometry']['location']
                entry.lat = (loc1['lat'] + loc2['lat']) / 2
                entry.long = (loc1['lng'] + loc2['lng']) / 2
                streetData[intersection_string] = {'lat':entry.lat, 'long':entry.long}
            else:
                entry.lat = streetData[intersection_string]['lat']
                entry.long = streetData[intersection_string]['long']
    save(traffic_data, 'traffic_data.pickle')
    save(zeroEntries, 'zeroEntries.pickle') 
    save(zeroDatesToStreets, 'zeroDatesToStreets.pickle')

def find_distance(first, second):
    lat = first.lat - second.lat
    lng = first.long - second.long
    return math.sqrt((lat*lat) + (lng*lng))

def main():
    traffic_data = load('traffic_data.pickle')
    zeroDatesToStreets = load('zeroDatesToStreets.pickle')
    zeroEntries = load('zeroEntries.pickle')
    scores = {}
    locations = set([])
    # collect scores for zeroEntries
    for entry in zeroEntries:
        corresponding_day_data = zeroDatesToStreets[entry.date]
        zero_time_intervals = [index for index, time_traffic in enumerate(entry.traffic) if time_traffic == 0.0]
        score, other_locations = calculateScore(entry, corresponding_day_data, zero_time_intervals)
        scores[entry] = ({"score": score, "time_intervals": zero_time_intervals, "other_locations": other_locations})
        locations |= (set([val["segmentID"] for val in other_locations]))
    # collect score for rest of data
    locationData = {location: [] for location in locations}
    for row in traffic_data:
        if row.segmentID in locations:    
            locationData[row.segmentID].append(row)
    # score location for each entry
    for key, val in scores.iteritems():
        score = 0.0
        for location in val["other_locations"]:
            corresponding_entries = locationData[location["segmentID"]]
            entry_score = 0.0
            for entry in corresponding_entries:
                entry_score += sum([entry.traffic[index] for index in val["time_intervals"]])
            score += entry_score / (len(corresponding_entries) * location["distance"])
        val["avg_score"] = score
    avg_differntial = 0
    for key,score in scores.iteritems():
        avg_differntial += score["avg_score"] - score["score"]
    print float(avg_differntial) / len(score.keys())


def calculateScore(entry, corresponding_day_data, zero_time_intervals):
    score = 0.0
    other_locations = []
    for val in corresponding_day_data:
        dist = find_distance(entry, val)
        if dist != 0.0:
            other_locations.append({"segmentID": val.segmentID, "distance": dist})
            score += sum([val.traffic[index] for index in zero_time_intervals]) / dist
    return score, other_locations

if __name__ == "__main__":
    # getAndCleanData()
    main()
