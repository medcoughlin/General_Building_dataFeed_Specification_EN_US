import plotly.graph_objects as go
import numpy as np
import pandas as pd
def draw_data(file):
    df=pd.read_csv(file)
    df=df[(pd.notna(df['Latitude']))|(pd.notna(df['Longitude']))]
    df['Latitude']= pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude']=pd.to_numeric(df['Longitude'], errors='coerce')
    df['Unique Building Identifier'] = pd.to_numeric(df['Unique Building Identifier'], errors='coerce')
    print(df['Unique Building Identifier'].dtype)
    df.drop(df[np.isnan(df['Longitude'])].index, inplace=True)
    df.drop(df[np.isnan(df['Latitude'])].index, inplace=True)
    df.drop(df[np.isnan(df['Unique Building Identifier'])].index, inplace=True)
    city_data = df[['Unique Building Identifier','Latitude', 'Longitude']]
    # print(city_data.values.tolist())
    # print(city_data[['Unique Building Identifier']].values.tolist())
    # 假设 CSV 文件中包含 'city', 'latitude', 'longitude' 列 # 将城市的经纬度等信息转换为适用于地图绘制的格式
    map_data = {'locations': city_data[['Latitude', 'Longitude']].values.tolist(),'cities':city_data[['Unique Building Identifier']].values.tolist()}
    fig = go.Figure()
    names = []
    # 添加散点图层，使用经纬度数据标记建筑物位置
    fig.add_trace(go.Scattergeo(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=8,
            color='blue',
            opacity=0.8
        ),
        text=df,  # 设置显示的文本，可以根据需求修改
        hoverinfo='text',
    ))

    # 设置地图布局
    fig.update_layout(
        title='美国地图',
        geo=dict(
            scope='usa',
            projection_type='albers usa'
        )
    )

    return fig
