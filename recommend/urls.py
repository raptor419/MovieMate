import django.urls

from . import views

urlpatterns = [
    django.urls.path('', views.index, name='index'),
    django.urls.path('<int:movie_id>/', views.detail, name='detail'),
    django.urls.path('signup/', views.signUp, name='signup'),
    django.urls.path('login/', views.Login, name='login'),
    django.urls.path('logout/', views.Logout, name='logout'),
    django.urls.path('recommend/', views.recommend, name='recommend')
]