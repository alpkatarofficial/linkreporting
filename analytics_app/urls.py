from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_view, name='analytics'),
    path('download/', views.download_chart, name='download_chart'),

]
