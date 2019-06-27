# search.views.py
from itertools import chain
from django.views.generic import ListView

from app_user.models import ProfileTraveler, ProfileHost
from app_main.models import Trip


class SearchView(ListView):
    template_name = 'app_search/view.html'
    paginate_by = 10
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        checked_traveler = self.request.GET.get('traveler')
        checked_host = self.request.GET.get('host')

        if query is not None and checked_host is not None and checked_traveler is None:
            res_host = ProfileHost.objects.search(query)
            qs = sorted(res_host,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        elif query is not None and checked_host is None and checked_traveler is not None:
            res_traveler = ProfileTraveler.objects.search(query)
            res_trip = Trip.objects.search(query)
            # combine querysets
            qs = list(res_traveler) + list(res_trip)
            self.count = len(qs)  # since qs is actually a list
            return qs
        elif query is not None and checked_host is not None and checked_traveler is not None:
            res_traveler = ProfileTraveler.objects.search(query)
            res_host = ProfileHost.objects.search(query)
            res_trip = Trip.objects.search(query)
            # combine querysets
            qs = list(res_traveler)+list(res_host)+list(res_trip)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return ProfileTraveler.objects.none()  # just an empty queryset as default
