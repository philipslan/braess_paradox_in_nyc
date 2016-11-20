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
    zeroEntries = set([])
    zeroDates = set([])

    # Find all entries that have 0 traffic at some point in the day
    for entry in data:
        e = TrafficEntry(entry)
        if 0.0 in e.traffic:
            zeroEntries.add(e)

    # Find all dates at which at least 1 road has 0 traffic at some point in the day
    for e in zeroEntries:
        if e.date not in zeroDates:
            zeroDates.add(e.date)

    # Find number of traffic entries for each zeroDate
    for date in zeroDates:
        entries = set([])
        for entry in data:
            e = TrafficEntry(entry)
            if date == e.date:
                entries.add(e)

        print date, len(entries)

main()
