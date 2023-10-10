import folium

# Define the LONLAT coordinates and number of locations
locations = [
    (113.891800, 22.127899),
    (113.893700, 22.131401),
    (113.892502, 22.130899),
    (113.891998, 22.129200),
    (113.717201, 21.922001),
    (113.715897, 21.917200),
    (113.713501, 21.909599),
    (113.740097, 21.928801),
    (113.746597, 21.921400),
    (113.751900, 21.940800),
    (113.759003, 21.941000),
    (113.768097, 21.941101),
    (113.721397, 21.959499),
    (113.721397, 21.966900),
]

locations_2 = [
    (112.84, 21.54),
    (113.7758, 22.0936),
]

locations_3 = [
    (113.707680, 21.924143),
    (113.727791, 21.921230),
    (113.744865, 21.939873),
    (113.731079, 21.952072),
    (113.717407, 21.958010),
    (113.702187, 21.947491)
]

# Create a base map
m = folium.Map(location=[22.127899, 113.891800], zoom_start=12)  # 设置tiles为None，以删除默认的OpenStreetMap底图

# # 使用高德地图的瓦片
# amap_tile = 'http://webst02.is.autonavi.com/appmaptile?style=7&x={x}&y={y}&z={z}'
# folium.TileLayer(tiles=amap_tile, attr="Amap", name="Amap").add_to(m)

# Add the points to the map
for idx, (lon, lat) in enumerate(locations_2, 1):
    folium.Marker([lat, lon], popup=str(idx), tooltip=str(idx)).add_to(m)

# # Add the points from locations_2 list with circles
# for lon, lat in locations_2:
#     folium.Circle(
#         location=[lat, lon],
#         radius=300,  # radius in meters, adjust as needed
#         fill=True,
#         fill_color='#3186cc',
#         fill_opacity=0.6,
#     ).add_to(m)

# Save the map to an HTML file
m.save('map_波浪浮标.html')
