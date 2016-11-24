#libraries
import rdflib
from rdflib import URIRef, Literal, Namespace, plugin, Graph, ConjunctiveGraph
from rdflib.store import Store

class Utils:
    def __init__(self, g):
        self.g = g
        self.prefixes = {'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
            'foaf': 'http://xmlns.com/foaf/0.1/',
            'geom': 'http://geovocab.org/geometry#',
            'transit': 'http://vocab.org/transit/terms/',
            'locn': 'http://www.w3.org/ns/locn#',
            'vcard': 'http://www.w3.org/2006/vcard/ns#',
            'dcterms': 'http://purl.org/dc/terms/',
            'schema': 'http://schema.org/',
            'geosparql': 'http://www.opengis.net/ont/geosparql#',
            'unknown': 'http://data.linkedevents.org/def/unknown#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'dul': 'http://ontologydesignpatterns.org/ont/dul/DUL.owl#',
            'naptan': 'http://transport.data.gov.uk/def/naptan/',
            'xsd': 'http://www.w3.org/2001/XMLSchema#',
            'owl': 'http://www.w3.org/2002/07/owl#',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'locationOnt': 'http://data.linkedevents.org/def/location#',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'travel': 'http://3cixty.com/ontology#',
            'qb': 'http://purl.org/linked-data/cube#',
            'dct': 'http://purl.org/dc/terms/',
            'sf': 'http://www.opengis.net/ont/sf#'}

    def bindingPrefixes(self):
        for key in self.prefixes:
            self.g.bind(key, self.prefixes[key])
        return self.g

class RDF:
    def __init__(self):
        self.geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
        self.foaf = Namespace("http://xmlns.com/foaf/0.1/")
        self.geom = Namespace("http://geovocab.org/geometry#")
        self.unknown = Namespace("http://data.linkedevents.org/def/unknown#")
        self.transit = Namespace("http://vocab.org/transit/terms/")
        self.locn = Namespace("http://www.w3.org/ns/locn#")
        self.vcard = Namespace('http://www.w3.org/2006/vcard/ns#')
        self.dcterms = Namespace("http://purl.org/dc/terms/")
        self.schema = Namespace('http://schema.org/')
        self.geosparql = Namespace("http://www.opengis.net/ont/geosparql#")
        self.rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
        self.naptan = Namespace('http://transport.data.gov.uk/def/naptan/')
        self.xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
        self.owl = Namespace('http://www.w3.org/2002/07/owl#')
        self.rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.locationOnt = Namespace("http://data.linkedevents.org/def/location#")
        self.dul = Namespace('http://ontologydesignpatterns.org/ont/dul/DUL.owl#')
        self.dc = Namespace('http://purl.org/dc/elements/1.1/')
        self.travel = Namespace('http://3cixty.com/ontology#')
        self.qb = Namespace('http://purl.org/linked-data/cube#')
        self.dct = Namespace('http://purl.org/dc/terms/')
        self.sf = Namespace("http://www.opengis.net/ont/sf#")

        self.store = plugin.get('IOMemory', Store)()
        self.g = Graph(self.store)
        self.graph = ConjunctiveGraph(self.store)

class Tube(RDF):
    def __init__(self, x, y, station, description, wkt, businessType, publisher, lines):
        RDF.__init__(self)
        self.tubes = ['Bakerloo',
                          'Central',
                          'Circle',
                          'District',
                          'Hammersmith & City',
                          'Jubilee',
                          'Metropolitan',
                          'Northern',
                          'Piccadilly',
                          'Victoria',
                          'Waterloo & City']

        for i in self.tubes:
            tubeline = URIRef('http://data.linkedevents.org/transit/London/subwayRoute/' + Literal(i).replace(" ", ""))
            self.g.add((tubeline, self.rdf.type, self.transit.SubwayRoute))

        self.x = x
        self.y = y
        self.station = str(station).strip()
        self.description = str(description).strip()
        self.wkt = wkt
        self.businessType = businessType
        self.publisher = publisher
        self.lines = lines

    def createStation(self):
        stationName = URIRef('http://data.linkedevents.org/transit/London/subwayStop/' + Literal(self.station).replace(" ", ""))
        return stationName

    def createStationGeom(self):
        stationGeom = URIRef(self.createStation() + '/geometry')
        return stationGeom

    def addStationLine(self):
        for i in self.lines:
            singleLine = URIRef('http://data.linkedevents.org/transit/London/subwayRoute/' + Literal(i).replace(" ", ""))
            self.g.add((self.createStation(), self.transit.route, singleLine))
        return self.g

    def createTubeGraph(self):
        name = self.createStation()
        geom = self.createStationGeom()

        self.g.add((name, self.rdf.type, self.transit.Station))
        self.g.add((name, self.rdf.type, self.dul.Place))
        self.g.add((name, self.rdfs.label, Literal(self.station)))
        self.g.add((name, self.dct.description, Literal(self.description)))
        self.g.add((name, self.geo.location, geom))
        self.g.add((name, self.locationOnt.businessType, URIRef(Literal(self.businessType))))
        self.g.add((name, self.dc.publisher, URIRef(Literal(self.publisher))))
        self.g.add((geom, self.rdf.type, self.geo.Point))
        self.g.add((geom, self.geo.lat, Literal(self.y, datatype=self.xsd.double)))
        self.g.add((geom, self.geo.long, Literal(self.x, datatype=self.xsd.double)))
        self.g.add((geom, self.locn.geometry, Literal(self.wkt, datatype=self.geosparql.wktLiteral)))

        self.addStationLine()
        return self.g

class TimeBetween(Tube):
    def __init__(self, id, origin, time, destination):
        RDF.__init__(self)
        self.id = id
        self.origin = str(origin).strip()
        self.time = time
        self.destination = str(destination).strip()

    def createTimeBetween(self):
        timeBetween = URIRef('http://data.linkedevents.org/travel/London/timeBetween#' + Literal(self.id))
        return timeBetween

    def overrideCreateStation(self, name):
        stationName = URIRef('http://data.linkedevents.org/transit/London/subwayStop/' + Literal(name).replace(" ", ""))
        return stationName

    def createTimeGraph(self):
        timeBetween = self.createTimeBetween()

        origin = self.overrideCreateStation(self.origin)
        destination = self.overrideCreateStation(self.destination)

        self.g.add((timeBetween, self.rdf.type, self.qb.Observation))
        self.g.add((timeBetween, self.travel.origin, origin))
        self.g.add((timeBetween, self.travel.destination, destination))
        self.g.add((timeBetween, self.travel.travelTime, Literal(self.time, datatype=self.xsd.int)))
        return self.g

class Bus(RDF):
    def __init__(self, stopId, stopGUID, x, y, label, wkt, addressLocality, adminUnit, publisher, businessType):
        RDF.__init__(self)
        self.stopId = stopId
        self.stopGUID = stopGUID
        self.x = x
        self.y = y
        self.label = label
        self.wkt = wkt
        self.addressLocality = addressLocality
        self.adminUnit = adminUnit
        self.publisher = publisher
        self.businessType = businessType

    def createBusStop(self):
        busStop = URIRef("http://data.linkedevents.org/transit/London/stop/" + Literal(self.stopId))
        return busStop

    def createGeometry(self):
        busStopGeom = URIRef('http://data.linkedevents.org/location/' + Literal(self.stopGUID) + '/geometry')
        return busStopGeom

    def createAddress(self):
        stopAddress = URIRef('http://data.linkedevents.org/location/' + Literal(self.stopGUID) + '/address')
        return stopAddress

    def createLabel(self):
        title = Literal(str(self.label).title())
        return title

    def createBusGraph(self):
        busStop = self.createBusStop()
        address = self.createAddress()
        geom = self.createGeometry()
        label = Literal(self.createLabel())

        self.g.add((busStop, self.rdf.type, self.naptan.BusStop))
        self.g.add((busStop, self.rdf.type, self.dul.Place))
        self.g.add((busStop, self.rdf.type, self.transit.Stop))
        self.g.add((busStop, self.dc.identifier, Literal(self.stopId)))
        self.g.add((busStop, self.geom.geometry, geom))

        self.g.add((address, self.rdf.type, self.schema.PostalAddress))
        self.g.add((address, self.rdf.type, self.dcterms.Location))
        self.g.add((address, self.dcterms.title, label))
        self.g.add((address, self.schema.streetAddress, label))
        self.g.add((address, self.locn.address, label))
        self.g.add((address, self.schema.addressLocality, Literal(self.addressLocality)))
        self.g.add((address, self.locn.adminUnit12, Literal(self.adminUnit)))

        self.g.add((geom, self.rdf.type, self.geo.Point))
        self.g.add((geom, self.geo.lat, Literal(self.y, datatype=self.xsd.double)))
        self.g.add((geom, self.geo.long, Literal(self.x, datatype=self.xsd.double)))
        self.g.add((geom, self.locn.geometry, Literal(self.wkt, datatype=self.geosparql.wktLiteral)))

        self.g.add((busStop, self.geo.location, geom))
        self.g.add((busStop, self.schema.location, address))
        self.g.add((busStop, self.locn.address, address))
        self.g.add((busStop, self.dc.publisher, Literal(self.publisher)))
        self.g.add((busStop, self.locationOnt.businessType, Literal(self.businessType)))
        self.g.add((busStop, self.rdfs.label, label))
        return self.g

class Busline(Bus):
    def __init__(self, route, run, wkt, label):
        RDF.__init__(self)
        self.route = route
        self.run = run
        self.wkt = Literal(wkt)
        self.label = Literal(str(label).title())

    def createBusline(self):
        busline = URIRef('http://data.linkedevents.org/transit/London/busLine/' + Literal(self.route))
        return busline

    def createBuslineGeom(self):
        buslineGeom = URIRef(self.createBusline() + '/geometry')
        return buslineGeom

    def createRoute(self):
        busRoute = URIRef('http://data.linkedevents.org/transit/London/route/' + Literal(self.route))
        return busRoute

    def createRouteService(self):
        routeService = URIRef('http://data.linkedevents.org/transit/London/service/' + Literal(self.route) + '_' + Literal(self.run))
        return routeService

    def createBuslineGraph(self):
        busline = self.createBusline()
        geom = self.createBuslineGeom()
        route = self.createRoute()
        service = self.createRouteService()
        label = self.createLabel()

        self.g.add((busline, self.rdf.type, self.transit.BusRoute))
        self.g.add((busline, self.geo.location, geom))
        self.g.add((busline, self.rdfs.label, label))
        self.g.add((busline, self.transit.RouteService, service))
        self.g.add((busline, self.transit.route, route))
        self.g.add((geom, self.rdf.type, self.sf.LineString))
        self.g.add((geom, self.locn.geometry, self.wkt))
        return self.g

class BusCorrespondence(Busline):
    def __init__(self, stopId, route, run, sequence):
        RDF.__init__(self)
        self.stopId = stopId
        self.route = route
        self.run = run
        self.sequence = sequence
        self.service = str(route) + '_' + str(run)

    def createServiceStop(self):
        serviceStopId = URIRef('http://data.linkedevents.org/transit/London/serviceStop/' + Literal(self.service) + '/' + Literal(self.stopId))
        return serviceStopId

    def createService(self):
        service = URIRef('http://data.linkedevents.org/transit/London/service/' + Literal(self.service))
        return service

    def createBusCorrespondenceGraph(self):
        servStop = self.createServiceStop()
        stop = self.createBusStop()
        serv = self.createService()

        self.g.add((servStop, self.rdf.type, self.transit.ServiceStop))
        self.g.add((servStop, self.transit.service, serv))
        self.g.add((servStop, self.transit.sequence, Literal(self.sequence, datatype=self.xsd.int)))
        self.g.add((servStop, self.transit.stop, stop))
        return self.g

class Area(RDF):
    def __init__(self, name, code, geom):
        RDF.__init__(self)
        self.name = str(name).strip()
        self.code = str(code).strip()
        self.geom = geom

    def createArea(self):
        area = URIRef('http://data.linkedevents.org/transit/London/area/' + Literal(self.code))
        return area

    def createAreaGeom(self):
        areaGeom = URIRef(self.createArea() + '/geometry')
        return areaGeom

    def createAreaGraph(self):
        area = self.createArea()
        geom = self.createAreaGeom()
        self.g.add((area, self.rdf.type, self.schema.AdministrativeArea))
        self.g.add((area, self.rdfs.label, Literal(self.name.title())))
        self.g.add((area, self.dct.identifier, Literal(self.code)))
        self.g.add((area, self.geo.location, geom))
        self.g.add((geom, self.locn.geometry, Literal(self.geom)))
        return self.g

def main(myGraph):
    content = myGraph
    utils = Utils(content)
    utils.bindingPrefixes()
    #content.serialize(destination='/Users/Agata/Desktop/tube.ttl', format='turtle')
    #print('The file in place.')
    print(content.serialize(format='turtle'))