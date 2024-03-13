from math import sin, cos, sqrt, atan2, radians, degrees, pi
from urllib import request
from django.shortcuts import render
import joblib
import datetime
import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

with open("./savedModels/model.pkl", 'rb') as f:
    model = pickle.load(f)


current_time = datetime.datetime.now()

longitude = []
latitude = []
R = 6373.0
jfk_lat = 40.641766
jfk_lng = -73.780968
ewr_lat = 40.689491
ewr_lng = -74.174538
lga_lat = 40.776863
lga_lng = -73.874069
sol_lat = 64.6197
sol_lng = -164.387
nyc_lat = 40.7128
nyc_lng = -74.0060


def main(request):
    latitude.append(request.GET.get('latitude'))
    longitude.append(request.GET.get('longitude'))
    for i in range(len(longitude)):
        if longitude[i] is None:
            del longitude[i]

        if latitude[i] is None:
            del latitude[i]
    if len(longitude) != 0:
        pickup_longitude = float(longitude[0])
        pickup_latitude = float(latitude[0])
        if len(longitude) >= 2:
            dropoff_longitude = float(longitude[1])
            dropoff_latitude = float(latitude[1])
    if len(latitude) >= 2:
        distance = get_dist(
            longitude[0], longitude[1], latitude[0], latitude[1])
        jfk_dist = get_dist(longitude[0], jfk_lng, latitude[0], jfk_lat)
        ewr_dist = get_dist(longitude[0], ewr_lng, latitude[0], ewr_lat)
        lga_dist = get_dist(longitude[0], lga_lng, latitude[0], lga_lat)
        sol_dist = get_dist(longitude[0], sol_lng, latitude[0], sol_lat)
        nyc_dist = get_dist(longitude[0], nyc_lng, latitude[0], nyc_lat)
        bearing = get_bearing(
            longitude[0], longitude[1], latitude[0], latitude[1])
        # can also get the avg distance between getin-airport and dropoff-airport depending on the actual meaning of the data
    fare = 0
    # if request.method == 'POST':
    sky, temp = get_weather_data()
    temp = int(temp[0])
    if request.method == 'POST':
        Car_condition = int(request.POST.get('Car_Condition'))
        passenger_count = int(request.POST.get('passenger_count'))
    Weather = get_weather(temp, sky)
    hour = current_time.hour
    day = current_time.day
    month = current_time.month
    weekday = current_time.day % 7
    year = current_time.year
    traffic = get_traffic(hour, weekday)
    Traffic_Condition_Congested_Traffic = bool(traffic[0])
    Traffic_Condition_Dense_Traffic = bool(traffic[1])
    Traffic_Condition_Flow_Traffic = bool(traffic[2])
    if len(latitude) >= 2:
        features = pd.DataFrame({
            'Car Condition': [Car_condition],
            'Weather': [Weather],
            'pickup_longitude': [pickup_longitude+73],
            'pickup_latitude': [pickup_latitude-40],
            'dropoff_longitude': [dropoff_longitude+73],
            'dropoff_latitude': [dropoff_latitude-40],
            'passenger_count': [passenger_count],
            'hour': [hour],
            'day': [day],
            'month': [month],
            'weekday': [weekday],
            'year': [year],
            'jfk_dist': [jfk_dist],
            'ewr_dist': [ewr_dist],
            'lga_dist': [lga_dist],
            'sol_dist': [sol_dist],
            'nyc_dist': [nyc_dist],
            'distance': [distance],
            'bearing': [bearing],
            'Traffic Condition_Congested Traffic': [Traffic_Condition_Congested_Traffic],
            'Traffic Condition_Dense Traffic': [Traffic_Condition_Dense_Traffic],
            'Traffic Condition_Flow Traffic': [Traffic_Condition_Flow_Traffic],
            # 'polyfeature': 1,
        })

        print(features)

        # norm_features = scaler.fit_transform(features)
        norm_fare = model.predict(features)
        print(norm_fare)
        fare = float(norm_fare[0]*42)
        print(fare)
        norm_fare = []
        fare = "{:.2f}".format(fare)
    context = {'fare': fare}
    return render(request, 'main.html', context)


def get_weather_data():
    url = "https://www.google.com/search?q="+"weather"+"nyc"+"&hl=en"
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = str.split('\n')
    sky = data[1]
    return sky, temp


def get_dist(lng1, lng2, lat1, lat2):
    dlng = float(lng2)-float(lng1)
    dlat = float(lat2)-float(lat1)
    lat1 = float(lat1)
    lat2 = float(lat2)
    a = (sin(dlat/2))**2 + \
        cos(lat1) * cos(lat2) * (sin(dlng/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


def get_bearing(lng1, lng2, lat1, lat2):
    """
    Calculates the bearing between two points as a compass bearing in radians
    and normalizes it to the range of -π to π radians.
    """
    lat1 = float(lat1)
    lat2 = float(lat2)
    lng2 = float(lng2)
    lng1 = float(lng1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    diff_lon = radians(lng2 - lng1)
    x = sin(diff_lon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(diff_lon)
    initial_bearing = atan2(x, y)
    if initial_bearing > pi:
        initial_bearing -= 2 * pi
    elif initial_bearing < -pi:
        initial_bearing += 2 * pi
    return initial_bearing


def get_traffic(time, weekday):
    if weekday > 2 and weekday < 6 and time > 9 and time < 16:
        return [1, 0, 0]
    elif time > 16 and time < 23:
        return [0, 1, 0]
    else:
        return [0, 0, 1]


def get_weather(temp, sky):
    if sky == 'Clear':
        return 1
    elif sky == 'Rain':
        return 2
    elif sky == 'Windy':
        return 4
    elif temp < 14:
        return 3
    elif temp > 17 and temp < 30:
        return 0


features = pd.DataFrame({
    'Car Condition': [2],
    'Weather': [-11],
    'pickup_longitude': [-1],
    'pickup_latitude': [1],
    'dropoff_longitude': [1],
    'dropoff_latitude': [4],
    'passenger_count': [1],
    'hour': [2],
    'day': [3],
    'month': [1],
    'weekday': [1],
    'year': [1],
    'jfk_dist': [1],
    'ewr_dist': [2],
    'lga_dist': [1],
    'sol_dist': [1],
    'nyc_dist': [4],
    'distance': [3],
    'bearing': [5],
    'Traffic Condition_Congested Traffic': [0],
    'Traffic Condition_Dense Traffic': [0],
    'Traffic Condition_Flow Traffic': [1],
    'polyfeature': 1,
})
