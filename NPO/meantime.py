import geopandas as gpd
from mizani.transforms import trans

major = [0, 1, 2]
t = trans()
print(t.minor_breaks(major))
t = trans(minor_breaks=[4])
# print(t.minor_breaks(major))
# print(minor_breaks(4))
gdf = gpd