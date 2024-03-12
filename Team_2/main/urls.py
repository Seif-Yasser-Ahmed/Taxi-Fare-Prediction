from django.urls import path
from . import views
# from map import views as map_views
urlpatterns = {
    path('', views.main, name='main'),
}
