from datetime import datetime
import json
import string

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
        for i in range(15, 39):
            self.traffic.append(float(dataEntry[i]))

def main():
    rawData = open('nyc_street_data.json')
    data = json.load(rawData)
    zeroEntries = []

    for entry in data:
        e = TrafficEntry(entry)
        if 0.0 in e.traffic:
            zeroEntries.append(e)

    for e in zeroEntries:
        print e.date

main()
