import csv, os, uuid, pyproj, random, string, rdflib, time, imp, re

from random import seed
from rdflib import URIRef, Literal, Namespace, plugin, Graph, BNode
from rdflib.store import Store

imp.load_source('common','/Users/patrick/3cixty/codes/3cixtyCommon/commonFunctions.py')
from common import readCsv, getUid, ConvertProj, definePrefixes, bindingPrefixes, readDict
from time import strftime

os.chdir('/Users/patrick/3cixty/codes/3cixtyHotel/airbnbModule/london/') # @patrick CASA Mac setup
print os.getcwd()


if not os.path.exists('DATA/'):
    os.makedirs('DATA/')


start_time = time.time()

def readCsv(inputfile):
    try:
        f = open(inputfile, 'rU')
        rf = csv.reader(f, delimiter=',')
        return rf
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise

def getUid(r0):#use this script to create NON-COMPLIANT uuid
    hotelUri = Namespace("http://data.linkedevents.org/places/london/hotels")
    idencode = r0.encode('utf-8')
    uid = uuid.uuid5(hotelUri, idencode)
    return uid


def definePrefixes():
    prefixes = {'acco': 'http://purl.org/acco/ns#',
                'dc': 'http://purl.org/dc/elements/1.1/',
                'dct': 'http://purl.org/dc/terms/',
                'dul': 'http://ontologydesignpatterns.org/ont/dul/DUL.owl#',
                'geom': 'http://geovocab.org/geometry#',
                'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
                'gr': 'http://purl.org/goodrelations/v1#',
                'gsp': 'http://www.opengis.net/ont/geosparql#',
                'locationOnt': 'http://data.linkedevents.org/def/location#',
                'locationRes': 'http://data.linkedevents.org/location/',
                'locn': 'http://www.w3.org/ns/locn#',
                'owl':'http://www.w3.org/2002/07/owl#',
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'schema': 'http://schema.org/',
                'threecixtyKOS':'http://data.linkedevents.org/kos/3cixty/',
                'time': 'http://www.w3.org/2006/time#',
                'xsd': 'http://www.w3.org/2001/XMLSchema#',}
    return prefixes

def bindingPrefixes(g, prefixes):
    for key in prefixes:
        g.bind(key, prefixes[key])
    return g

def createHotelId(hotelId):
    hotelId = URIRef('http://data.linkedevents.org/london/hotels/' + hotelId)
    return hotelId

def createLocationResId(objectId):#USE THIS SCRIPT TO GENERATE QNAME COMPLIANT UUID
    hotelUri = Namespace("http://data.linkedevents.org/places/london/hotels")
    idencode = objectId.encode('utf-8')
    uid = uuid.uuid5(hotelUri, idencode)
    puid = URIRef("http://data.linkedevents.org/location/" + Literal(uid))
    uuidList = list(puid)
    chars = string.ascii_letters
    pwdSize = 1
    random.seed(101) #set seed so the random number generated is replicable in the next iteration
    newId = ''.join((random.choice(chars)) for x in range(pwdSize))
    uuidList[38] = newId
    locationResID = ''.join(uuidList).lower()

    return locationResID

def getHotelData(row):
    hotelId = row[0]
    #hotelName = str(row[1])#.encode('ascii',errors='ignore')
    hotelName = re.sub('[^a-zA-Z0-9\n\.]', ' ', str(row[1]))
    hotelGUID = createLocationResId(row[0])
    hotelHostId = row[2]
    hotelHostName = row[3]
    hotelNghbrhood = row[4]
    hotelLat = row[5]
    hotelLong = row[6]
    hotelGeom = "POINT (" + str(hotelLat) + " " + str(hotelLong) + ")"
    hotelRoomTyp = row[7]
    hotelPrice = row[8]
    hotelMinNights=row[9]
    hotelNoReview=row[10]
    hotelLastReview=row[11]
    hotelReviewMonth= row[12]
    hotelCalcListing=row[13]
    hotelYrlyAvblty=row[14]
    hotelPublisher = URIRef('https://www.airbnb.co.uk')
    hotelBusinessType = URIRef('http://data.linkedevents.org/kos/3cixty/hotel')

    lst = [hotelId, hotelName, hotelGUID, hotelHostId, hotelHostName, hotelNghbrhood,
           hotelLat, hotelLong, hotelGeom, hotelRoomTyp, hotelPrice, hotelMinNights,
           hotelNoReview, hotelLastReview, hotelReviewMonth, hotelCalcListing, hotelYrlyAvblty,
           hotelPublisher, hotelBusinessType]
    return lst

def createHotelGraph(arg, g):
    acco = Namespace("http://purl.org/acco/ns#")
    dc = Namespace("http://purl.org/dc/elements/1.1/")
    dct = Namespace('http://purl.org/dc/terms/')
    dul= Namespace('http://ontologydesignpatterns.org/ont/dul/DUL.owl#')
    geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
    gr = Namespace('http://purl.org/goodrelations/v1#')
    gs = Namespace("http://www.opengis.net/ont/geosparql#")
    locationOnt = Namespace("http://data.linkedevents.org/def/location#")
    locn = Namespace("http://www.w3.org/ns/locn#")
    owl = Namespace('http://www.w3.org/2002/07/owl#')
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    schema = Namespace("http://schema.org/")
    threecixtyKOS = Namespace('http://data.linkedevents.org/kos/3cixty/')
    xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

    locationRes = URIRef(arg[2])
    singleGeometry = URIRef("http://data.linkedevents.org/location/" + "%s" + "/geometry") % getUid(arg[0])
    singleAddress = URIRef("http://data.linkedevents.org/location/" + "%s" + "/address") % getUid(arg[0])

    g.add((locationRes, rdf.type, dul.place))
    g.add((locationRes, rdfs.label, Literal(arg[1])))
    g.add((locationRes, locationOnt.businessType, threecixtyKOS.residence))
    g.add((locationRes, dc.identifier, Literal(arg[0])))
    g.add((locationRes, dc.publisher, arg[17]))

    g.add((locationRes, owl.sameAs, URIRef("http://www.airbnb.co.uk/rooms/" + "%s") % arg[0]))
    g.add((locationRes, schema.location, singleAddress))
    g.add((locationRes, geo.location, singleGeometry))

    g.add((singleGeometry, rdf.type, geo.Point))
    g.add((singleGeometry, geo.lat, Literal(arg[6], datatype=xsd.placeholder)))
    g.add((singleGeometry, geo.long, Literal(arg[7], datatype=xsd.placeholder)))
    g.add((singleGeometry, locn.geometry, Literal(arg[8], datatype=gs.wktLiteral)))

    g.add((singleAddress, rdf.type, schema.postalAddress))
    #g.add((singleAddress, dct.title, Literal(arg[1])))
    g.add((singleAddress, schema.addressCountry, Literal('uk')))
    g.add((singleAddress, schema.addressLocality, Literal(arg[5])))


    prefixes=definePrefixes()
    bindingPrefixes(g, prefixes)

    return g

def createConHotelGraph(arg, g):
    dul = Namespace("http://ontologydesignpatterns.org/ont/dul/DUL.owl#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    locationRes = URIRef("http://data.linkedevents.org/location/" + Literal(arg[12]))
    g.add((locationRes, rdf.type, dul.place))

    return g

def main():
    pathf = "./"
    inFile = pathf + "DATA/airbnbLondon_validated.csv"

    outFile = pathf + "DATA/airbnb_Londondirty.ttl"

    csv = readCsv(inFile)
    next(csv, None)  # FILE WITH HEADERS

    store = plugin.get('IOMemory', Store)()
    g = Graph(store)

    prefixes = definePrefixes()
    print('Binding Prefixes')
    bindingPrefixes(g, prefixes)

    print('Creating graph-Hotel...')  # AMENDED

    #This one generates the 'turtle' graph. Please deactivate the script for the 'nt' graph below
    for row in csv:
        lstData = getHotelData(row)
        createHotelGraph(lstData, g).serialize(outFile, format='turtle')

    print ('DONE! Time elapsed ' + str((time.time() - start_time)))

if __name__ == "__main__":
    main()
