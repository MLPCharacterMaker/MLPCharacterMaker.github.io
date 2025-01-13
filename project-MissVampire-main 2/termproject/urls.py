"""
URL configuration for termproject project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from charactercreator import views  # Import your app's views

urlpatterns = [
    path('characters/', views.character_list, name='character-list'),
    path('characters/create/', views.create_character, name='create-character'),
    path('characters/edit/<int:pk>/', views.edit_character, name='edit-character'),
    path('characters/view/<int:pk>/', views.view_character, name='view-character'),
    path('login/', auth_views.LoginView.as_view(template_name='charactercreator/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('map/', views.map, name='map'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
