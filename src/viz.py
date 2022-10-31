import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import geopandas as gpd
from cartoframes.viz import Map, Layer
from pymongo import MongoClient
from pymongo import GEOSPHERE
import plotly.express as px
import re


def scatter(df,x,title):
    fig = px.scatter(df, x = x, y = 'Apertura de un negocio', trendline="ols", trendline_scope="overall", color = 'Economía', hover_name = 'Economía', height=500, width=700, title=title)
    return fig.show()


def get_points_of_interest(y_lat,y_long,req):
    load_dotenv()
    token_fsq = os.getenv("token")
    df_locations=pd.DataFrame(columns=['Name','Category','Latitude','Longitude','Distance','Address'])

    for keys, values in req.items():
        if type(values['cat_id'])==int:
            url = f"https://api.foursquare.com/v3/places/search?ll={y_lat}%2C{y_long}&radius={values['distance']}&categories={values['cat_id']}&sort={values['sort']}&limit=5"
        else:
            url = f"https://api.foursquare.com/v3/places/search?query={values['cat_id']}&ll={y_lat}%2C{y_long}&radius={values['distance']}&sort={values['sort']}&limit=5"
        headers = {
            "Accept": "application/json",
            "Authorization": token_fsq
        }

        response = requests.get(url, headers=headers)

        name=[]
        category=[]
        lat=[]
        long=[]
        distance=[]
        address=[]

        for i in range(len(response.json()["results"])):
            name.append(response.json()["results"][i]['name'])
            try:
                category.append(response.json()["results"][i]['categories'][0]['name'])
            except:
                category.append('')
            lat.append(response.json()["results"][i]['geocodes']['main']['latitude'])
            long.append(response.json()["results"][i]['geocodes']['main']['longitude'])
            distance.append(response.json()["results"][i]['distance'])
            address.append(response.json()["results"][i]['location']['formatted_address'])

        loc_list=list(zip(name, category, lat, long, distance,address))
        df_=pd.DataFrame(loc_list,columns=['Name','Category','Latitude','Longitude','Distance','Address'])
        df_['Requirement']=keys
        df_
        df_locations=pd.merge(df_locations,df_,how='outer')    
        
    return df_locations




def map_markers(map,df):

    for index, row, in df.iterrows():
        district={"location":[row["Latitude"], row["Longitude"]], "tooltip":row["Requirement"]}
        # 1. Education
        if row['Requirement']=='school':
            icon= Icon(color="red", prefix="fa", icon="graduation-cap", icon_color="black")
        # 2. Starbucks
        elif row['Requirement']=='starbucks':
            icon= Icon(color="green", prefix="fa", icon="coffee", icon_color="black")
        # 3. Bar
        elif row['Requirement']=='bar':
            icon= Icon(color="lightblue", prefix="fa", icon="glass", icon_color="black")
        # 4. Club
        elif row['Requirement']=='club':
            icon= Icon(color="purple", prefix="fa", icon="music", icon_color="black")
        # 5. Airport
        elif row['Requirement']=='Airport':
            icon= Icon(color="blue", prefix="fa", icon="plane", icon_color="black")    
        # 6. Vegan
        elif row['Requirement']=='vegan':
            icon= Icon(color="beige", prefix="fa", icon="leaf", icon_color="black")
        # 7. Basketball
        elif row['Requirement']=='basketball':
            icon= Icon(color="orange", prefix="fa", icon="futbol-o", icon_color="black")
        # 8. Pet grooming
        elif row['Requirement']=='pet grooming':
            icon= Icon(color="white", prefix="fa", icon="paw", icon_color="black")
         # 9. Design company
        elif row['Requirement']=='design company':
            icon= Icon(color="pink", prefix="fa", icon="pencil", icon_color="black")
        # 9. Tech company
        elif row['Requirement']=='tech company':
            icon= Icon(color="lightgray", prefix="fa", icon="code", icon_color="black")
        
        new_marker=Marker(icon=icon, **district)
        new_marker.add_to(map)

    return map