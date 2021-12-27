from django.urls import path
from .views import HomeView,HelpView,StatisticsView,recordsView
urlpatterns =[
    path('',HomeView,name="home"),
    path('pomoc/',HelpView,name="help"),
    path('statystki/',StatisticsView,name="stats"),
    path('archiwum/',recordsView,name="records")
]