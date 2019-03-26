from django.urls import path, include
from django.conf.urls import url
from . import views, update_db
from ohsiha_app.views import TestPageView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.HomePageView, name='kotisivu'),
    path('testi/', TestPageView.as_view(), name='testisivu'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('palvelu/', views.PalveluView, name='palvelu'),
    path('palvelu/paivita_junadata', update_db.junadataTietokantaan, name="paivita_junadata"),
]


