import urllib3
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

sparql.setQuery("""
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo:  <http://dbpedia.org/ontology>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
PREFIX dc:   <http://purl.org/dc/elements/1.1/>

SELECT DISTINCT ?birthdate ?thumbnail ?author ?name ?description
WHERE {
    ?author rdf:type dbo:Writer ;
            dbo:birthdate ?birthdate ;
            rdfs:label ?name ;
            rdfs:comment ?description
    FILTER (
        (lang(?name)="en") && (lang(?description)="en") 
        && (STRLEN(STR(?birthdate)) > 6)
        && (SUBSTR(STR(?birthdate), 6) = SUBSTR(STR(bif:curdate('')), 6))
    ) .
    OPTIONAL { ?author dbo:thumbnail ?thumbnail .}
}
ORDER BY ?birthdate
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Create HTML output
print('<html><head><title>Literary Birthdays of Today</title></head>')

# Extract Weekday %A / Month %B /Day of the Month %d by formating today's date accordingly
datum = datetime.today().strftime("%A %B %d")
print ('<body><1>Literary Birthdays of {}</h1>'.format(datum))

print('<ul>')

for result in results["results"]["bindings"]:
    if "author" in result:
        # Create Wikipedia Link
        wikiurl = "http://en.wikipedia.org/wiki" + result["author"]["value"].encode('ascii', 'ignore').split('/')[-1]
    else:
        wikiurl = 'NONE'
    if "name" in result:
        name = result["name"]["value"].encode('ascii', 'ignore')
    else:
        name = 'NONE'
    if "birthdate" in result:
        date = result["birthdate"]["value"].encode('ascii', 'ignore')
    else:
        date = 'NONE'
    if "description" in result:
        description = result["description"]["value"].encode('ascii', 'ignore')
    else:
        description = ' '
    if "thumbnail" in result:
        pic = result["thumbnail"]["value"].encode('ascii', 'ignore')
    else:
        pic = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Question_mark2.svg/71px-Question_mark2.svg.png'

    # Parse date as datetime
    dt = datetime.strptime(date, '%Y-%m-%d')
    print(
        '<li><b>{}</b> -- <img src="{}" height="60px"> <a href="{}">{}</a>, {} </li>'. format(
            dt.year, pic.replace("300", "60"), wikiurl, name, description
        )
    )

    print('</ul>')
    print('</body></html>')