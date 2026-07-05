from django.urls import path
from . import views
urlpatterns = [
    path('upload_photo/',views.upload_photo,name="upload"),
    path('display_photo/',views.display,name="photo"),
    
]
