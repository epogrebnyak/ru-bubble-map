# %%
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


plt.figure(figsize=(12, 9))
ax = plt.axes(
    projection=cartopy.crs.TransverseMercator(
        central_longitude=57,
        central_latitude=37,
    )
)
ax.add_feature(cartopy.feature.BORDERS, linestyle="-", alpha=1)
ax.coastlines(resolution="110m")
ax.add_feature(cartopy.feature.OCEAN, facecolor=(0.5, 0.5, 0.5))
ax.gridlines()
ax.set_extent((30, 80, 36, 69), cartopy.crs.PlateCarree())
plt.show()

# %%

from cartopy.crs import Mercator
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 9))
m = Mercator(
    central_longitude=40,
    min_latitude=35,
    max_latitude=84.0,
    globe=None,
    latitude_true_scale=35,
    false_easting=0.0,
    false_northing=0.0,
    scale_factor=None,
)
ax = plt.axes(projection=m)
ax.set_extent((25, 80, 36, 69), cartopy.crs.PlateCarree())
ax.stock_img()
plt.show()


# %%
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

ax = plt.axes(projection=ccrs.Mollweide())
ax.stock_img()
plt.show()

# %%
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()

ny_lon, ny_lat = -75, 43
delhi_lon, delhi_lat = 77.23, 28.61

plt.plot(
    [ny_lon, delhi_lon],
    [ny_lat, delhi_lat],
    color="blue",
    linewidth=2,
    marker="o",
    transform=ccrs.Geodetic(),
)

plt.plot(
    [ny_lon, delhi_lon],
    [ny_lat, delhi_lat],
    color="gray",
    linestyle="--",
    transform=ccrs.PlateCarree(),
)

plt.text(
    ny_lon - 3,
    ny_lat - 12,
    "New York",
    horizontalalignment="right",
    transform=ccrs.Geodetic(),
)

plt.text(
    delhi_lon + 3,
    delhi_lat - 12,
    "Delhi",
    horizontalalignment="left",
    transform=ccrs.Geodetic(),
)

plt.show()


# %%
