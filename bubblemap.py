import warnings
warnings.filterwarnings('ignore', message='numpy.dtype size changed') # fix warnings bug
import pandas as pd
import plotly
import topojson # pip install git+https://github.com/sgillies/topojson.git
import requests
import json

# limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
# colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
# cities = []
# scale = 5000

# for i in range(len(limits)):
#     lim = limits[i]
#     df_sub = df[lim[0]:lim[1]]
#     city = dict(
#         type = 'scattergeo',
#         locationmode = 'USA-states',
#         lon = df_sub['lon'],
#         lat = df_sub['lat'],
#         text = df_sub['text'],
#         marker = dict(
#             size = df_sub['pop']/scale,
#             color = colors[i],
#             line = dict(width=0.5, color='rgb(40,40,40)'),
#             sizemode = 'area'
#         ),
#         name = '{0} - {1}'.format(lim[0],lim[1]) )
#     cities.append(city)

# layout = dict(
#         title = '2014 US city populations<br>(Click legend to toggle traces)',
#         showlegend = True,
#         geo = dict(
#             scope='world',
#             projection=dict( type='albers usa' ),
#             showland = True,
#             landcolor = 'rgb(217, 217, 217)',
#             subunitwidth=1,
#             countrywidth=1,
#             subunitcolor="rgb(255, 255, 255)",
#             countrycolor="rgb(255, 255, 255)"
#         ),
#     )

# Russia example:

def get_geojson_data(filename):
    with open(filename) as json_file:
        data = json_file.read()
        geoJSON = json.loads(data)
        return geoJSON

def get_topojson_data(url):
    r = requests.get('https://raw.githubusercontent.com/zarkzork/russia-topojson/master/russia.json')
    if r.status_code != 200:
        print('Can not read topojson from url') 
        exit()

    return r.json()

def topo2geo(topoJSON):
    scale = topoJSON['transform']['scale']
    translation = topoJSON['transform']['translate']
    topo_features = topoJSON['objects']['subunits']['geometries']

    # convert topojson to geojson
    geoJSON = dict(type='FeatureCollection', features=[])
    for k, tfeature in enumerate(topo_features):
        # print(k, tfeature)
        geo_feature = dict(id=k, type='Feature')
        geo_feature['properties'] = tfeature['properties']
        geo_feature['geometry'] = topojson.geometry(tfeature, topoJSON['arcs'], scale, translation)
        geoJSON['features'].append(geo_feature)

    return geoJSON

def get_geo_points(geoJSON):
    pts = []
    for feature in geoJSON['features']:
        if feature['geometry']['type'] == 'Polygon':
            pts.extend(feature['geometry']['coordinates'][0])
            pts.append([None, None])

        elif feature['geometry']['type'] == 'MultiPolygon':
            for polyg in feature['geometry']['coordinates']:
                pts.extend(polyg[0])
                pts.append([None, None])
        else:
            print('Error: geometry type `{}` irrelevant for map'.format(feature['geometry']['type']))

    return pts


# geoJSON = get_geojson_data('./Russia_AL2.GeoJson') # get data from getJSON file
# url = 'https://raw.githubusercontent.com/Kreozot/russian-geo-data/master/topo.json'
url = 'https://raw.githubusercontent.com/zarkzork/russia-topojson/master/russia.json'
topoJSON = get_topojson_data(url) # get from url
geoJSON = topo2geo(topoJSON) # convert topoJSON to geoJSON
crimea_geoJSON = get_geojson_data('./crimea_9sr.json') # get crimea points

pts = get_geo_points(geoJSON) # main Russia geo points
crimea_pts = get_geo_points(crimea_geoJSON) # Crimea geo points
pts.extend(crimea_pts)

X, Y = zip(*pts)
data = [dict(
    type='scattergeo',
    lon=X, 
    lat=Y, 
    mode='lines', 
    line=dict(width=0.5, color='blue')
)]

lat1 = 55 + 45/60 + 21/(60*60)
lon1 = 37 + 37/60 + 4/(60*60)

city = dict(
    type = 'scattergeo',
    locationmode = 'country names',
    lon = [lon1],
    lat = [lat1],
    text = 'Moscow',
    marker = dict(
        size = [1200],
        color ='rgb(0,116,217)',
        line = dict(width=0.5, color='rgb(40,40,40)'),
        sizemode = 'area'
    ),
    name = 'Moscow' )
data.append(city)

layout = dict(
    title = 'City populations',
    showlegend = True,
    geo = dict(
        scope = 'world',
        # lonaxisRange=[10, 100],
        # lataxisRange=[20, 70],
        lonaxis = dict(range = [30.0, 190.0]),
        lataxis = dict(range = [30.0, 80.0]),
        # projection = dict(type = 'Mercator'),
        # projection = dict(type = 'azimuthal equal area'),
        # projection = dict(type = 'kavrayskiy7'),
        projection = dict(type = 'albers siberia'),
        showland = True,
        landcolor = 'rgb(217, 217, 217)',
        subunitwidth=1,
        countrywidth=1,
        subunitcolor = "rgb(255, 255, 255)",
        countrycolor = "rgb(255, 255, 255)",
        # center = dict(ion=37 + 37/60 + 4/(60*60), lat=55 + 45/60 + 21/(60*60)),
    ),
)

# fig = dict(data=[city], layout=layout)
fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, validate=False, filename='world.html')


# TODO: 
# 1. limit this map to Russia 
# 2. add topojson/geojson to display Russia


#Links:

#- https://toster.ru/q/328285
#- https://github.com/zarkzork/russia-topojson/blob/master/russia.json
#- https://plot.ly/~empet/14397/plotly-plot-of-a-map-from-data-available/#/
# https://habr.com/post/181766/