# ru-bubble-map
City population bubble map for Russia

Objectves
=========

1. Draw map of Russia with administrative borders in a conventional projection
2. Add cities as circles, circle size proportional to city population 
3. Collect sources and uses of economic locational data (cellular network use, 
   power consumption, transport, illumination, etc) 

   
Steps
=====   
   
- Formalise visual requirements for a map 
- Create city population and geoposition dataset 
- Make visualsations in python using different libraries
- Maintain list of data sources used 
- Make reading list of useful GIS-related links 

Mindmap
=======

Bits of GIS wisdom accululated so far:

- drawings are either JavaScript-based (bokeh, plotly, Altair) or raster-based (matplotlib), Al
- js libraries usually look smoother, but there is some ambiguity on how they render, saving to file is tricky
- Earth is an ellipsoid, unwrapping it to flat map requires a choice of projection
- you need a background picture of a map and some poligons for the administritive map
- what is the difference between topojson and geojson?



Links
=====

GIS tutorials
-------------


Other
-----

- https://toster.ru/q/328285
- https://github.com/zarkzork/russia-topojson/blob/master/russia.json
- https://plot.ly/~empet/14397/plotly-plot-of-a-map-from-data-available/#/
- http://gis-lab.info/qa/rusbounds-rosreestr-gen.html
- https://worldmap.harvard.edu/data/geonode:crimea_9sr

----------

- http://www.datadependence.com/2016/06/creating-map-visualisations-in-python/
- https://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html
- https://python-graph-gallery.com/313-bubble-map-with-folium/
- http://geopandas.readthedocs.io/en/latest/mapping.html
- https://blog.prototypr.io/interactive-maps-with-python-part-1-aa1563dbe5a9
- https://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html
- http://flowingdata.com/2009/11/12/how-to-make-a-us-county-thematic-map-using-free-tools/
- https://antonfromperm.wordpress.com/2009/11/25/how-to-make-a-russian-regional-thematic-map/
- https://sashat.me/2017/04/21/what-happened-to-soviet-cities/
- https://pypi.org/project/geopy/
