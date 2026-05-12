from django.urls import path
from . import views


urlpatterns = [
    path('' ,views.index,name="index"),
    path('create/' ,views.create_blog,name="create_blog"),
    path('dashboard/' ,views.dashboard,name="dashboard"),
    path('detail/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('edit/<slug:slug>/', views.blog_edit, name='blog_edit'),
    path('delete/<slug:slug>/', views.blog_delete, name='blog_delete'),
    path('test/', views.test, name='test'),


]