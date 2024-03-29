"""Plot Russia bubble map with plotly.

Similar to https://plot.ly/python/bubble-maps/

Has functions for topojson/geojson conversions.

"""
import os
import json
import plotly
import topojson
import requests


def get_json_local(filename):
    with open(filename) as json_file:
        data = json_file.read()
        return json.loads(data)


def get_json_remote(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    raise Exception("Cannot read topojson from {url}".format(url))


# FIXME: есть какие-то ссылки на алгоритм, откуда он берется? какие есть альтернативы?
def topo2geo(topoJSON: dict) -> dict:
    scale = topoJSON["transform"]["scale"]
    translation = topoJSON["transform"]["translate"]
    topo_features = topoJSON["objects"]["subunits"]["geometries"]
    # convert topojson to geojson
    geoJSON = dict(type="FeatureCollection", features=[])
    for k, tfeature in enumerate(topo_features):
        geo_feature = dict(id=k, type="Feature")
        geo_feature["properties"] = tfeature["properties"]
        geo_feature["geometry"] = topojson.geometry(
            tfeature, topoJSON["arcs"], scale, translation
        )
        geoJSON["features"].append(geo_feature)
    return geoJSON


# FIXME: тот же вопрос
def get_geo_points(geoJSON: dict) -> list:
    pts = []
    for feature in geoJSON["features"]:
        if feature["geometry"]["type"] == "Polygon":
            pts.extend(feature["geometry"]["coordinates"][0])
            pts.append([None, None])
        elif feature["geometry"]["type"] == "MultiPolygon":
            for polyg in feature["geometry"]["coordinates"]:
                pts.extend(polyg[0])
                pts.append([None, None])
        else:
            print(
                "Error: geometry type `{}` irrelevant for map".format(
                    feature["geometry"]["type"]
                )
            )
    return pts


TOPOJSON_URL = (
    "https://raw.githubusercontent.com/zarkzork/russia-topojson/master/russia.json"
)
CRIMEA_JSON_PATH = os.path.join("data", "crimea_9sr.json")
# get from url
topoJSON = get_json_remote(TOPOJSON_URL)
# convert topoJSON to geoJSON
geoJSON = topo2geo(topoJSON)
crimea_geoJSON = get_json_local(CRIMEA_JSON_PATH)

# main Russia geo points
pts = get_geo_points(geoJSON)
# Crimea geo points
crimea_pts = get_geo_points(crimea_geoJSON)
pts.extend(crimea_pts)

# make data for the graph, it includes the admin division + city bubbles
X, Y = zip(*pts)
data = [
    dict(
        type="scattergeo",
        lon=X,
        lat=Y,
        mode="lines",
        line=dict(width=0.5, color="blue"),
    )
]

# Moscow cooidinates
lat1 = 55 + 45 / 60 + 21 / (60 * 60)
lon1 = 37 + 37 / 60 + 4 / (60 * 60)

scaling_factor = 0.005
city = dict(
    type="scattergeo",
    locationmode="country names",
    lon=[lon1],
    lat=[lat1],
    text="Moscow",
    marker=dict(
        size=[12000 * scaling_factor],
        color="rgb(0,116,217)",
        line=dict(width=0.5, color="rgb(40,40,40)"),
        sizemode="area",
    ),
    name="Moscow",
)
data.append(city)

layout = dict(
    title="City populations",
    showlegend=True,
    # autosize = False,
    width=1200,
    height=800,
    # center = dict(lon=106, lat=64),
    geo=dict(
        scope="world",
        lonaxis=dict(range=[30.0, 200.0]),
        lataxis=dict(range=[30.0, 80.0]),
        projection=dict(type="miller"),
        showland=True,
        landcolor="rgb(217, 217, 217)",
        subunitwidth=1,
        countrywidth=1,
        subunitcolor="rgb(255, 255, 255)",
        countrycolor="rgb(255, 255, 255)",
        center=dict(lon=106, lat=64),
    ),
)


OUT_HTML = os.path.join("output", "russia.html")
fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, validate=False, filename=OUT_HTML)

# import plotly.plotly as py
# plotly.plotly.iplot(fig, validate=False, filename='world.html')

# Woah there! Look at all those points! Due to browser limitations, the Plotly SVG drawing functions have a hard time graphing more than 500k data points for line charts, or 40k points for other types of charts. Here are some suggestions:
# (1) Use the `plotly.graph_objs.Scattergl` trace object to generate a WebGl graph.
# (2) Trying using the image API to return an image instead of a graph URL
# (3) Use matplotlib
# (4) See if you can create your visualization with fewer data points

# If the visualization you're using aggregates points (e.g., box plot, histogram, etc.) you can disregard this warning.


# WONTFIX: world.html неверно ограничивает страну + отрывает Камчатку

"""
projections:

"equirectangular" | "mercator" | "orthographic" | "natural earth" | "kavrayskiy7" | "miller" | 
"robinson" | "eckert4" | "azimuthal equal area" | "azimuthal equidistant" | "conic equal area" | 
"conic conformal" | "conic equidistant" | "gnomonic" | "stereographic" | "mollweide" | "hammer" | 
"transverse mercator" | "albers usa" | "winkel tripel" | "aitoff" | "sinusoidal"
"""

### 1. FIXME: есть какие-то ссылки на алгоритм, откуда он берется? какие есть альтернативы?
#
# Алгоритм взят полностью из статьи приведенной в конце файла с примером: https://plot.ly/~empet/14397/plotly-plot-of-a-map-from-data-available/#/
# К сожалению я не нашел для python актуальных модулей, по этому для конвертации topojson в geojson правильней всего использовать модуль для node https://github.com/topojson/topojson
#
### 2. QUESTION: вопрос откуда plotly понимает эту проекцию, если она не в списке разрешенных?
#
# Было предположение, что раз есть `albers usa`, то может быть и `albers siberia`. Ошибок при интерпретации нет, но судя по всему при таком значении используется дефолтная проекция вроде Mercator.
#
### 3. world.html неверно ограничивает страну + отрывает Камчатку
#
# Дело в неправильном выборе масштаба и центровке карты, из-за сильного сдвига вправо камчатка отрывается и вылазит слева. Я сделал коммит где задал координаты центровки карты, это должно помочь, но нужно проверить на большом экране.
