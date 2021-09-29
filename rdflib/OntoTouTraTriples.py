import os
import pandas as pd
import rdflib
from rdflib.namespace import FOAF, DCTERMS, XSD, RDF, SDO
from rdflib import URIRef, BNode, Literal, Namespace

path = '/home/jf/Documentos/education/phd/thesis/dev/ontologies/protege/mysql csv data/'
cities_filename = os.path.join(path, 'city.csv')
cities_df = pd.read_csv(cities_filename)

path = '/home/jf/Documentos/education/phd/thesis/dev/ontologies/protege/'
g = rdflib.Graph()
onto_filename = os.path.join(path, 'ontotoutra with hotels.owl')

format_ = rdflib.util.guess_format(onto_filename)
g.parse(onto_filename, format=format_)

#print(f'Graph g has {len(g)} facts')
#print(g.serialize().decode('u8'))

#for s, p, o in g:
#    print(s, p, o)
#    break

qres = g.query('''
prefix xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX my:   <http://tourdata.org/ontotoutra/ontotoutra.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?stateID ?stateName
WHERE {
  ?state my:stateID ?stateID     ;
         my:stateName ?stateName .
}
''')

states = {}
for stateID, stateName in qres:
    states[stateID.value] = stateName

ott = Namespace('http://tourdata.org/ontotoutra/ontotoutra.owl#')
h = rdflib.Graph()
h.bind('ott', ott)

for index, row in cities_df.iterrows():
    cityID    = row['cityID']
    cityName  = row['cityName']
    stateID   = row['stateID']
    stateName = ott + states[stateID]

    city = ott[cityName.replace(" ", "")]
    h.add((city, RDF.type, ott.City))
    h.add((city, ott.hasStateParent, Literal(stateName)))
    h.add((city, ott.cityID, Literal(cityID, datatype=XSD.integer)))
    h.add((city, ott.cityName, Literal(cityName)))
    h.add((city, ott.stateID, Literal(stateID, datatype=XSD.integer)))

    print(row)
    print(h.serialize(format='xml').decode('u8'))
    print(h.serialize(format='ttl').decode('u8'))

    break