"""proj_travelshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from app_user import views as user_views
from app_search.views import SearchView
from django.contrib.auth.views import (LogoutView, LoginView, PasswordResetView,
                                       PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_main.urls')),

    path('search/', SearchView.as_view(), name='search'),

    path('register/', user_views.viewregister, name='register'),
    path('login/', LoginView.as_view(template_name="app_user/login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name="app_user/logout.html"), name="logout"),
    path('password-reset/', PasswordResetView.as_view(template_name="app_user/password_reset.html"),
       name="password_reset"),
    path('password-reset/done/',
       PasswordResetDoneView.as_view(template_name="app_user/password_reset_done.html"),
       name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
       PasswordResetConfirmView.as_view(template_name="app_user/password_reset_confirm.html"),
       name="password_reset_confirm"),
    path('password-reset-complete/',
       PasswordResetCompleteView.as_view(template_name="app_user/password_reset_complete.html"),
       name="password_reset_complete"),


    path('index/', user_views.viewindex, name='index'),
    path('profile_update_host/', user_views.profile_update_host, name='profile_update_host'),
    path('profile_update_host2/', user_views.profile_update_host2, name='profile_update_host2'),
    path('profile_update_host3/', user_views.profile_update_host3, name='profile_update_host3'),

    path('space_add/', user_views.space_add, name='space_add'),
    path('space_update/<int:space_id>/', user_views.space_update, name='space_update'),
    path('space_delete/<int:space_id>/', user_views.space_delete, name='space_delete'),
    path('space_detail/<int:space_id>/', user_views.space_detail, name='space_detail'),
    path('space_list/<int:userid>/', user_views.space_list, name='space_list'),

    path('profile_update_traveler/', user_views.profile_update_traveler, name='profile_update_traveler'),
    path('profile_update_traveler2/', user_views.profile_update_traveler2, name='profile_update_traveler2'),
    path('profile_update_traveler3/', user_views.profile_update_traveler3, name='profile_update_traveler3'),

    path('program_add/', user_views.program_add, name='program_add'),
    path('program_update/<int:program_id>/', user_views.program_update, name='program_update'),
    path('program_delete/<int:program_id>/', user_views.program_delete, name='program_delete'),
    path('program_detail/<int:program_id>/', user_views.program_detail, name='program_detail'),
    path('program_list/<int:userid>/', user_views.program_list, name='program_list'),

    path('profile_traveler/<int:userid>', user_views.profile_traveler, name='profile_traveler'),
    path('profile_host/<int:userid>/', user_views.profile_host, name='profile_host'),

    path('address_update/', user_views.address_update, name='address_update'),

    path('link_add/', user_views.link_add, name='link_add'),
    path('link_update/<int:link_id>/', user_views.link_update, name='link_update'),
    path('link_delete/<int:link_id>/', user_views.link_delete, name='link_delete'),
    path('link_detail/<int:link_id>/', user_views.link_detail, name='link_detail'),
    path('link_list/<int:userid>/', user_views.link_list, name='link_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
