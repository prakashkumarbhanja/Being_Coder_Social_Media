from django.urls import path
from . import views
urlpatterns = [
    path('homepage/', views.userhome_page, name='home_page'),
    path('createpost/', views.postcreate, name='createpost'),
    # path('/<int:id>/', views.Delete_Post.as_view(), name='deletepost'),
    path('deletepost/<int:id>/', views.delete_post, name='deletepost'),
    path('userprofile/<str:username>/', views.user_profile, name='userprofile'),

    path('likes/<int:id>/', views.likes, name='likes'),
    path('removelike/<int:id>/', views.remove_like, name='removelike'),

    path('followuser/<str:username>/', views.follow_user, name='followuser'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
]