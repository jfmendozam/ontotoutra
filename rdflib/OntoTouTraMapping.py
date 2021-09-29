# import plotly.graph_objects as go
# import pandas as pd

# df_airports = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
# print(df_airports.head())

# df_flight_paths = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_aa_flight_paths.csv')
# print(df_flight_paths.head())

# fig = go.Figure()

# fig.add_trace(go.Scattergeo(
#     locationmode = 'USA-states',
#     lon = df_airports['long'],
#     lat = df_airports['lat'],
#     hoverinfo = 'text',
#     text = df_airports['airport'],
#     mode = 'markers',
#     marker = dict(
#         size = 2,
#         color = 'rgb(255, 0, 0)',
#         line = dict(
#             width = 3,
#             color = 'rgba(68, 68, 68, 0)'
#         )
#     )))

# flight_paths = []
# for i in range(len(df_flight_paths)):
#     fig.add_trace(
#         go.Scattergeo(
#             locationmode = 'USA-states',
#             lon = [df_flight_paths['start_lon'][i], df_flight_paths['end_lon'][i]],
#             lat = [df_flight_paths['start_lat'][i], df_flight_paths['end_lat'][i]],
#             mode = 'lines',
#             line = dict(width = 1, color = 'red'),
#             opacity = float(df_flight_paths['cnt'][i]) / float(df_flight_paths['cnt'].max()),
#         )
#     )

# fig.update_layout(
#     title_text = 'Feb. 2011 American Airline flight paths<br>(Hover for airport names)',
#     showlegend = False,
#     geo = dict(
#         scope = 'north america',
#         projection_type = 'azimuthal equal area',
#         showland = True,
#         landcolor = 'rgb(243, 243, 243)',
#         countrycolor = 'rgb(204, 204, 204)',
#     ),
# )

# fig.show()


import os
import pandas as pd
import rdflib
from rdflib.namespace import FOAF, DCTERMS, XSD, RDF, SDO
from rdflib import URIRef, BNode, Literal, Namespace

path = '/home/jf/Documentos/education/phd/thesis/dev/ontologies/protege/'
g = rdflib.Graph()
onto_filename = os.path.join(path, 'ontotoutra.owl')

format_ = rdflib.util.guess_format(onto_filename)
g.parse(onto_filename, format=format_)

qres = g.query('''
prefix xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX ott:  <http://tourdata.org/ontotoutra/ontotoutra.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?hotelID ?cityName ?stateName ?score ?lat ?lon
WHERE {
  ?hotel ott:hotelID          ?hotelID   ;
         ott:hotelLat         ?lat       ;
         ott:hotelLon         ?lon       ;
         ott:hotelReviewScore ?score     ;
         ott:hasCityParent    ?city      .
  ?city  ott:cityID           ?cityID    ;
         ott:cityName         ?cityName  ;
         ott:hasStateParent   ?state     .
  ?state ott:stateName        ?stateName .
}
''')

city_data = []
for hotel, city, state, score, lat, lon in qres:
    if len(city.value) > 0:
        city_data.append([hotel.value, city.value, state.value, score.value, lat.value, lon.value])
city_df = pd.DataFrame(city_data, columns = ['Hotel', 'City', 'State', 'Score', 'lat', 'lon'])

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
token_filename = os.path.join(dir_path, ".mapbox_token")
token = open(token_filename).read() # token from Mapbox

import plotly.express as px

fig = px.scatter_mapbox(
    city_df, 
    lat="lat", 
    lon="lon", 
    hover_name="City", 
    hover_data=["State", "Score"],
    color_discrete_sequence=["fuchsia"], 
    zoom=5, 
    height=1000
)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_image("OntoTouTraMap.svg")
fig.show()