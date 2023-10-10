import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime

# 读取数据
data = pd.read_csv('浮标数据2021-2022.CSV', low_memory=False)
data_cleaned = data.dropna(subset=['Lat', 'Lon'])

# 定义站点颜色，确保不使用淡蓝色
all_stations = data_cleaned['Station_Id_C'].unique().tolist()
colors = ['#E6194B', '#3CB44B', '#FFE119', '#0082C8', '#F58231', '#911EB4', '#46F0F0', '#F032E6', '#D2D2D2', '#FABEBE']
colors = [c for c in colors if c != '#46F0F0']  # 移除淡蓝色
station_colors = dict(zip(all_stations, colors * (len(all_stations) // len(colors) + 1)))

# 创建动态地图对象
m_dynamic_actual = folium.Map(location=[data['Lat'].mean(), data['Lon'].mean()], zoom_start=7)

# 为每个站点创建一个时间戳的GeoJSON轨迹
features_actual = []
for station, color in station_colors.items():
    station_data = data_cleaned[data_cleaned['Station_Id_C'] == station].sort_values(by=['Year', 'Mon', 'Day'])

    for _, row in station_data.drop_duplicates(subset=['Year', 'Mon', 'Day']).iterrows():
        popup_content = "<br>".join([f"<b>{col}:</b> {row[col]}" for col in row.index])

        # 根据波高和波周期确定图标形状
        if row['Wave_Heigh_Max_Etime'] == 999999 and row['Wave_Heigh_Max_Period'] == 999999:
            continue  # 如果两者都是异常值，跳过该数据点
        elif row['Wave_Heigh_Max_Etime'] == 999999:
            icon_shape = 'star'  # 波高异常时，使用五角星形状
        elif row['Wave_Heigh_Max_Period'] == 999999:
            icon_shape = 'triangle'  # 波周期异常时，使用三角形形状
        else:
            icon_shape = 'circle'  # 正常数据点使用圆形

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['Lon'], row['Lat']]
            },
            'properties': {
                'times': [datetime(int(row['Year']), int(row['Mon']), int(row['Day'])).strftime('%Y-%m-%dT00:00:00')],
                'style': {'color': color, 'weight': 2},
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': color,
                    'fillOpacity': 0.8,
                    'stroke': 'true',
                    'radius': 5,
                    'popupContent': popup_content
                }
            }
        }
        features_actual.append(feature)

# 将时间戳的GeoJSON轨迹添加到地图上，并加入弹出窗口信息
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features_actual},
    period='PT12H',  # Set the period to 1 day
    add_last_point=True,
    auto_play=True,
    loop=True,
    max_speed=5,
    loop_button=True,
    date_options='YYYY-MM-DD',
    time_slider_drag_update=True,
    duration="P1D"
).add_to(m_dynamic_actual)

# 添加一个永久显示的图例并调整位置以确保显示完整
legend_html = """
<div style="position: fixed; bottom: 40px; left: 10px; width: 150px; height: 250px; border:2px solid grey; z-index:9999; font-size:14px;">
    &nbsp;<b>站点颜色</b><br>
    {}
</div>
""".format(''.join(
    [f'&nbsp;<i class="fa fa-circle fa-1x" style="color:{color}"></i>&nbsp;{station}<br>' for station, color in
     station_colors.items()]))
m_dynamic_actual.get_root().html.add_child(folium.Element(legend_html))

#新增浮标点位
locations_2 = [
    (112.84, 21.54),
    (113.7758, 22.0936),
]

# Add the points to the map
for idx, (lon, lat) in enumerate(locations_2, 1):
    folium.Marker([lat, lon], popup=str(idx), tooltip=str(idx)).add_to(m_dynamic_actual)

# 保存带有弹出窗口信息的动态地图为HTML文件
m_dynamic_actual.save('fubiao_dynamic_actual_map_by_day.html')
