
from django.urls import path

from . import views
from .views import *
urlpatterns = [
    path('', views.sign_up_view, name='sign_up'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_request, name='logout'),
]