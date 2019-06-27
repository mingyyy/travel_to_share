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

from django.urls import path
from .views import home, travelers, hosts, trip, CalendarViewTrip, CalendarViewAvailable, \
    available, available_new, trip_list, available_list, info, CalendarViewTripPrivate, \
    CalendarViewAvailablePrivate, CalendarViewAvailableHost, CalendarViewTripTraveler, \
    trip_view, available_view, get_visa_info, contact

app_name = "app_main"

urlpatterns = [
    path('', home, name='home'),
    path('info/', info, name='info'),
    path('get_info/', get_visa_info, name='get_info'),
    path('contact/', contact, name='contact'),

    path('travelers/', travelers, name='travelers'),
    path('hosts/', hosts, name='hosts'),
    path('trip_list/', trip_list, name='trip_list'),
    path('available_list/', available_list, name='available_list'),

    path('calendar/trip/<int:userid>/', CalendarViewTrip.as_view(), name='calendar_trip'),
    path('calendar/available/<int:userid>/', CalendarViewAvailable.as_view(), name='calendar_available'),

    path('calendar/trip/traveler/<int:userid>/', CalendarViewTripTraveler.as_view(), name='calendar_trip_traveler'),
    path('calendar/available/host/<int:userid>/', CalendarViewAvailableHost.as_view(), name='calendar_available_host'),

    path('calendar/trip/private/<int:user_id>/', CalendarViewTripPrivate.as_view(), name='calendar_trip_private'),
    path('calendar/available/private/<int:user_id>/', CalendarViewAvailablePrivate.as_view(), name='calendar_available_private'),

    path('trip/edit/<int:trip_id>/', trip, name='trip_edit'),
    path('trip/detail/<int:trip_id>/', trip_view, name='trip_detail'),
    path('trip/new/', trip, name='trip_new'),
    path('available/edit/<int:available_id>/', available, name='available_edit'),
    path('available/detail/<int:available_id>/', available_view, name='available_detail'),
    path('available/new/', available_new, name='available_new'),
]