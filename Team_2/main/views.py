from urllib import request
from django.shortcuts import render
import joblib
import datetime

current_time = datetime.datetime.now()


def main(request):
    # cls = joblib.load('final_internship_data.csv')
    # lis = []
    # lis.append(request.GET['carCondition'],)
    return render(request, 'main.html')


'''
[
# 'Car Condition': request.GET['carCondition']
'Weather': 
'pickup_longitude':
'pickup_latitude':
'dropoff_longitude':
'dropoff_latitude',
# 'passenger_count': request.GET['passenger_count']
# 'hour': current_time.hour
# 'day': current_time.day
# 'month': current_time.month
# 'weekday': current_time.day%7
# 'year': current_time.year
'jfk_dist':
'ewr_dist':
'lga_dist':
'sol_dist':
'nyc_dist':
'distance':
'bearing':
'Traffic Condition_Congested Traffic':
'Traffic Condition_Dense Traffic':
'Traffic Condition_Flow Traffic':
]
'''


def User(request):
    username = request.GET['username']
    return render(request, 'user.html', {'name': username})
