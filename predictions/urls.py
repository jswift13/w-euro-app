from django.urls import path
from . import views

app_name = 'predictions'


urlpatterns = [
    path('',                         views.home,              name='home'),
    path('matchday/<int:matchday_id>/', views.create_prediction, name='create'),
    path('confirmation/<int:pk>/',      views.confirmation,     name='confirmation'),
    path('standings/',                  views.standings,        name='standings'),
    path('about/',                      views.about,            name='about'),
]