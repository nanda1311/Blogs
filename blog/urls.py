from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('', views.home, name="home"),
     path('about', views.about, name="about"),
     path('contact', views.contact, name="contact"),
     path('login', views.login, name="login"),
     path('logout', views.logout, name="logout"),
     path('signup', views.signup, name="signup"),
     path('edit-blog/<slug:slug>/', views.edit_blog, name="edit_blog"),
     path('blog/delete/<slug:slug>/', views.delete_blog, name='delete_blog'),
     path('my-profile', views.my_profile, name="my_profile"),
     path('blog/<slug:slug>/', views.blog_detail, name="blog_detail"),
     path('create-blog/', views.create_blog, name="create_blog"),
]
