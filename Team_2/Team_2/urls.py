from django.contrib import admin
from django.urls import include, path
# from . import views
# from main import views as map_views
urlpatterns = [
    path('', include('main.urls')),
    # path('', map_views.main, name='main'),
    path('admin/', admin.site.urls),
]
