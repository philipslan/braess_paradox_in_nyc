import json

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
        self.date = dataEntry[14]
        self.n12to1am = float(dataEntry[15])
        self.n1to2am = float(dataEntry[16])
        self.n2to3am = float(dataEntry[17])
        self.n3to4am = float(dataEntry[18])
        self.n4to5am = float(dataEntry[19])
        self.n5to6am = float(dataEntry[20])
        self.n6to7am = float(dataEntry[21])
        self.n7to8am = float(dataEntry[22])
        self.n8to9am = float(dataEntry[23])
        self.n9to10am = float(dataEntry[24])
        self.n10to11am = float(dataEntry[25])
        self.n11to12pm = float(dataEntry[26])
        self.n12to1pm = float(dataEntry[27])
        self.n1to2pm = float(dataEntry[28])
        self.n2to3pm = float(dataEntry[29])
        self.n3to4pm = float(dataEntry[30])
        self.n4to5pm = float(dataEntry[31])
        self.n5to6pm = float(dataEntry[32])
        self.n6to7pm = float(dataEntry[33])
        self.n7to8pm = float(dataEntry[34])
        self.n8to9pm = float(dataEntry[35])
        self.n9to10pm = float(dataEntry[36])
        self.n10to11pm = float(dataEntry[37])
        self.n11to12am = float(dataEntry[38])

def main():
    rawData = open('nyc_street_data.json')
    data = json.load(rawData)
    for entry in data:
        e = TrafficEntry(entry)
        print e.roadName


main()
