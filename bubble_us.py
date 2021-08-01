import os
import pandas as pd
import plotly


# prototype:

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv"
)
df["text"] = df["name"] + "<br>Population " + (df["pop"] / 1e6).astype(str) + " million"

limits = [(0, 2), (3, 10), (11, 20), (21, 50), (50, 3000)]
colors = [
    "rgb(0,116,217)",
    "rgb(255,65,54)",
    "rgb(133,20,75)",
    "rgb(255,133,27)",
    "lightgrey",
]
cities = []
scale = 5000

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0] : lim[1]]
    city = dict(
        type="scattergeo",
        locationmode="USA-states",
        lon=df_sub["lon"],
        lat=df_sub["lat"],
        text=df_sub["text"],
        marker=dict(
            size=df_sub["pop"] / scale,
            color=colors[i],
            line=dict(width=0.5, color="rgb(40,40,40)"),
            sizemode="area",
        ),
        name="{0} - {1}".format(lim[0], lim[1]),
    )
    cities.append(city)

layout = dict(
    title="2014 US city populations<br>(Click legend to toggle traces)",
    showlegend=True,
    geo=dict(
        scope="world",
        projection=dict(type="albers usa"),
        showland=True,
        landcolor="rgb(217, 217, 217)",
        subunitwidth=1,
        countrywidth=1,
        subunitcolor="rgb(255, 255, 255)",
        countrycolor="rgb(255, 255, 255)",
    ),
)

fig = dict(data=cities, layout=layout)
out_html = os.path.join("output", "d3-bubble-map-populations.html")
plotly.offline.plot(fig, validate=False, filename=out_html)
