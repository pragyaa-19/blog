"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path,include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static


def root_redirect(request):
    return redirect('index')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect),
    path('register/',views.register_user, name='register'),
    path('login/',views.login_user, name='login'),
    path('log-out/',views.logout_user, name='logout'),
    path('edit_profile/',views.edit_profile, name='edit'),
    path('user_profile/',views.user_Profile, name='profile'),
    path('blog/',include("homepage.urls")),
    path('photo/',include("photo_uploader.urls")),
    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

