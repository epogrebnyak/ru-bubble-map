import pandas as pd
import plotly


# prototype:

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
df['text'] = df['name'] + '<br>Population ' + (df['pop']/1e6).astype(str)+' million'

limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
cities = []
scale = 5000

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    city = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df_sub['lon'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['pop']/scale,
            color = colors[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1]) )
    cities.append(city)

layout = dict(
        title = '2014 US city populations<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope='world',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

#fig = dict( data=cities, layout=layout )
#plotly.offline.plot( fig, validate=False, filename='d3-bubble-map-populations.html' )



# Russia example:

layout = dict(
        title = 'City populations',
        showlegend = True,
        geo = dict(
            scope='world',
            #lonaxisRange=[10, 100],
            #lataxisRange=[20, 70],
            lonaxis = dict( range= [ 30.0, 190.0 ] ),
            lataxis = dict( range= [ 30.0, 80.0 ] ),
            projection=dict(type = 'Mercator'),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    ) 

"55°45′21″ с. ш. 37°37′04″ в. д."
lat1 = 55 + 45/60 + 21/(60*60)
lon1 = 37 + 37/60 + 4/(60*60)

city = dict(
    type = 'scattergeo',
    locationmode = 'country names',
    lon = [lon1],
    lat = [lat1],
    text = 'Moscow',
    marker = dict(
        size = [12000],
        color ='rgb(0,116,217)',
        line = dict(width=0.5, color='rgb(40,40,40)'),
        sizemode = 'area'
    ),
    name = 'Moscow' )

fig = dict(data=[city], layout=layout )        
plotly.offline.plot( fig, validate=False, filename='world.html' )        

# TODO: 
# 1. limit this map to Russia 
# 2. add topojson/geojson to display Russia


#Links:

#- https://toster.ru/q/328285
#- https://github.com/zarkzork/russia-topojson/blob/master/russia.json
#- https://plot.ly/~empet/14397/plotly-plot-of-a-map-from-data-available/#/
