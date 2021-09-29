from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:3030")

query = """
PREFIX my:   <http://tourdata.org/ontotoutra/ontotoutra.owl#>

SELECT ?stateID ?state
WHERE {
  ?state my:stateID ?stateCode ;
         my:stateName ?stateName .
  BIND (str(?stateCode) as ?stateID)
}
"""
sparql.setQuery(query)

#sparql.setQuery("""
#    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#    SELECT ?label
#    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
#"""
#)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["label"]["value"])

print('---------------------------')

for result in results["results"]["bindings"]:
    print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))