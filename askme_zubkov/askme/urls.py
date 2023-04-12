from django.urls import path

from .views import *

urlpatterns = [
    path('', index), # '' - корень относительного пути(в данном случае localhost/askme)
]

