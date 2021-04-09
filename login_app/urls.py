from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('username', views.username),
    path('login', views.login),
    path('logout', views.logout),
    path('trips', views.trips),
    path('add-trip', views.add_trip),
    path('create-trip', views.create_trip),
    path('<int:trip_id>/view', views.view_trip),
    path('<int:trip_id>/join', views.join_trip),
    path('<int:trip_id>/cancel', views.cancel_trip),
    path('<int:trip_id>/delete', views.delete_trip)
]
