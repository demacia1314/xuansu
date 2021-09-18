from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_developer,name='index_developer'),
    path('auth/',views.auth,name='auth')
]