from django.urls import path
from . import views


urlpatterns = [
    path('' ,views.index,name="index"),
    path('create_blog/' ,views.create_blog,name="create_blog"),
    path('dashboard/' ,views.dashboard,name="dashboard"),
    path('detail/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('edit/<slug:slug>/', views.blog_edit, name='blog_edit'),
    path('delete/<slug:slug>/', views.blog_delete, name='blog_delete'),
    path('about/', views.about, name='about'),
    path('explore/', views.explore, name='explore'),
    path("react/<int:blog_id>/",views.react_blog,name="react_blog"),
    path("author_profile/<str:username>/",views.author_profile,name="author_profile"),
    path('follow/', views.follow, name='follow'),
    path('save/', views.save, name='save'),
    path('saved/', views.saved, name='saved'),
    path('drafts/', views.drafts, name='drafts'),
    
    
    
    

]