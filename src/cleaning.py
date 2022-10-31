import os
import json
import pandas as pd
import numpy as np
from pymongo import MongoClient
from pymongo import GEOSPHERE
import re



def mongo():
    client = MongoClient("localhost:27017")
    db= client["ironhack"]
    companies=db.get_collection("companies")

    # startups
    query=[{"founded_year":{"$gte":2009}},{"number_of_employees":{"$gte":8}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    tech_comp = list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1))
   
    # design - category
    query=[{"category_code":"design"},{"number_of_employees":{"$gte":8}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    tech_comp.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))


    # design - "tag_list" 
    query=[{"tag_list":{"$regex":".*design.*"}},{"number_of_employees":{"$gte":8}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    tech_comp.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    # design - name
    query=[{"name":{"$regex":".*design.*"}},{"number_of_employees":{"$gte":8}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    tech_comp.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    # web - category
    query=[{"category_code":"web"},{"number_of_employees":{"$gte":8}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    tech_comp.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    # tech - category
    query=[{"category_code":"tech"},{"number_of_employees":{"$gte":8}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    tech_comp.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    # tech - category
    query=[{"name":{"$regex":".*tech.*"}},{"number_of_employees":{"$gte":8}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    tech_comp.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    df = pd.DataFrame(tech_comp)
    df=df.explode('offices')
    df.reset_index(inplace=True,drop=True)

    def office_country(dict_):
        try:
            if 'country_code' in dict_.keys():
                country=dict_['country_code']
            elif type(dict_)==str:
                country=dict__
        except:
            country=np.nan
        return country

    df['country']=df['offices'].apply(office_country)

    def office_city(dict_):
        try:
            if 'city' in dict_.keys():
                city=dict_['city']
            elif type(dict_)==str:
                city=dict__
        except:
            city=np.nan
        return city
    
    df['city']=df['offices'].apply(office_city)


    def office_lat(dict_):
        try:
            if 'latitude' in dict_.keys():
                lat=dict_['latitude']
            elif type(dict_)==str:
                lat=dict__
        except:
            lat=np.nan
        return lat
    
    df['lat']=df['offices'].apply(office_lat)


    def office_long(dict_):
        try:
            if 'longitude' in dict_.keys():
                long=dict_['longitude']
            elif type(dict_)==str:
                long=dict__
        except:
            long=np.nan
        return long

    df['long']=df['offices'].apply(office_long)

    df2=df.dropna(subset=['city','lat'])
    df3=df2.drop(columns=['offices'])
    df3.reset_index(inplace=True,drop=True)
    df3.drop(df3[df3['total_money_raised'] == '$0'].index, inplace=True)
    return df3