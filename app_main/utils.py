from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Trip, Available
from django.db.models import Q, F
from django.conf import settings


class CalendarTrip(HTMLCalendar):
    def __init__(self, year=None, month=None):
        super(CalendarTrip, self).__init__()
        self.year = year
        self.month = month

    def formatday(self, day, events):
        # events_per_day = events.filter(start_time__day__lte=day, end_time__day__gte=day)
        """
        code logic for the Day filter
        1. for events start and end in the same year
        start_time__year = current year = end_time__year & start_time__month = current month = end_time__month,
        start_time__day <= current day <= end_time__day
        OR
        start_time__year = current year = end_time__year & start_time__month < current month < end_time__month,
        OR
        start_time__year = current year = end_time__year & start_time__month = current month < end_time__month,
        start_time__day <= current day
        OR
        start_time__year = current year = end_time__year & start_time__month < current month = end_time__month,
        current day <= end_time__day
        2. for events start and end in different years
        start_time__year < current year < end_time__year
        OR
        start_time__year < current year = end_time__year & current month < end_time__month
        OR
        start_time__year < current year = end_time__year & current month = end_time__month,
        current day <= end_time__day
        OR
        start_time__year = current year < end_time__year & start_time__month < current month
        OR
        start_time__year = current year < end_time__year & start_time__month = current month
        start_time__day <= current day
        """
        events_per_day = events.filter(Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month=self.month, end_date__month=self.month,
                          start_date__day__lte=day, end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month__lt=self.month, end_date__month__gt=self.month)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month__lt=self.month, end_date__month=self.month,
                          end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month=self.month, end_date__month__gt=self.month,
                          start_date__day__lte=day)|
                        Q(start_date__year__lt=self.year, end_date__year__gt=self.year)|
                        Q(start_date__year__lt=self.year, end_date__year=self.year,
                          end_date__month__gt=self.month)|
                        Q(start_date__year__lt=self.year, end_date__year=self.year,
                          end_date__month=self.month, end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year__gt=self.year,
                          start_date__month__lt=self.month)|
                        Q(start_date__year=self.year, end_date__year__gt=self.year,
                          start_date__month=self.month, start_date__day__lte=day))
        d = ''
        for event in events_per_day:
            d += f'<li>{event.get_html_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True):

        events = Trip.objects.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                       start_date__month__lte=self.month, end_date__month__gte=self.month) |
                                     Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                     Q(start_date__year__lt=self.year, end_date__year=self.year,
                                        end_date__month__gte=self.month) |
                                     Q(start_date__year=self.year, end_date__year__gt=self.year,
                                        start_date__month__lte=self.month))
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal+'</table>'


class CalendarAvail(HTMLCalendar):
    def __init__(self, year=None, month=None):
        super(CalendarAvail, self).__init__()
        self.year = year
        self.month = month

    def formatday(self, day, events):

        events_per_day = events.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month=self.month, end_date__month=self.month,
                                         start_date__day__lte=day, end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month__lt=self.month, end_date__month__gt=self.month) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month__lt=self.month, end_date__month=self.month,
                                         end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month=self.month, end_date__month__gt=self.month,
                                         start_date__day__lte=day) |
                                       Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                       Q(start_date__year__lt=self.year, end_date__year=self.year,
                                         end_date__month__gt=self.month) |
                                       Q(start_date__year__lt=self.year, end_date__year=self.year,
                                         end_date__month=self.month, end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year__gt=self.year,
                                         start_date__month__lt=self.month) |
                                       Q(start_date__year=self.year, end_date__year__gt=self.year,
                                         start_date__month=self.month, start_date__day__lte=day))
        d = ''
        for event in events_per_day:
            d += f'<li>{event.get_html_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True):

        events = Available.objects.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                       start_date__month__lte=self.month, end_date__month__gte=self.month) |
                                     Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                     Q(start_date__year__lt=self.year, end_date__year=self.year,
                                       end_date__month__gte=self.month) |
                                     Q(start_date__year=self.year, end_date__year__gt=self.year,
                                       start_date__month__lte=self.month))
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal + '</table>'


class CalendarAvailPriv(HTMLCalendar):
    def __init__(self, year=None, month=None, **kwargs):
        super(CalendarAvailPriv, self).__init__(**kwargs)
        self.year = year
        self.month = month

    def formatday(self, day, events):
        events_per_day = events.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month=self.month, end_date__month=self.month,
                                         start_date__day__lte=day, end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month__lt=self.month, end_date__month__gt=self.month) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month__lt=self.month, end_date__month=self.month,
                                         end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month=self.month, end_date__month__gt=self.month,
                                         start_date__day__lte=day) |
                                       Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                       Q(start_date__year__lt=self.year, end_date__year=self.year,
                                         end_date__month__gt=self.month) |
                                       Q(start_date__year__lt=self.year, end_date__year=self.year,
                                         end_date__month=self.month, end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year__gt=self.year,
                                         start_date__month__lt=self.month) |
                                       Q(start_date__year=self.year, end_date__year__gt=self.year,
                                         start_date__month=self.month, start_date__day__lte=day))
        d = ''
        for event in events_per_day:
            d += f'<li>{event.get_html_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True,**kwargs):
        # User = settings.settings.AUTH_USER_MODEL

        events = Available.objects.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                       start_date__month__lte=self.month, end_date__month__gte=self.month) |
                                     Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                     Q(start_date__year__lt=self.year, end_date__year=self.year,
                                       end_date__month__gte=self.month) |
                                     Q(start_date__year=self.year, end_date__year__gt=self.year,
                                       start_date__month__lte=self.month)).filter(user_id=kwargs['user_id'])
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal + '</table>'


class CalendarTripPriv(HTMLCalendar):
    def __init__(self, year=None, month=None):
        super(CalendarTripPriv, self).__init__()
        self.year = year
        self.month = month


    def formatday(self, day, events):
        events_per_day = events.filter(Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month=self.month, end_date__month=self.month,
                          start_date__day__lte=day, end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month__lt=self.month, end_date__month__gt=self.month)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month__lt=self.month, end_date__month=self.month,
                          end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month=self.month, end_date__month__gt=self.month,
                          start_date__day__lte=day)|
                        Q(start_date__year__lt=self.year, end_date__year__gt=self.year)|
                        Q(start_date__year__lt=self.year, end_date__year=self.year,
                          end_date__month__gt=self.month)|
                        Q(start_date__year__lt=self.year, end_date__year=self.year,
                          end_date__month=self.month, end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year__gt=self.year,
                          start_date__month__lt=self.month)|
                        Q(start_date__year=self.year, end_date__year__gt=self.year,
                          start_date__month=self.month, start_date__day__lte=day))
        d = ''
        for event in events_per_day:
            d += f'<li>{event.get_html_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True, **kwargs):

        events = Trip.objects.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                       start_date__month__lte=self.month, end_date__month__gte=self.month) |
                                     Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                     Q(start_date__year__lt=self.year, end_date__year=self.year,
                                        end_date__month__gte=self.month) |
                                     Q(start_date__year=self.year, end_date__year__gt=self.year,
                                        start_date__month__lte=self.month)).filter(user_id=kwargs['user_id'])

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal+'</table>'


class CalendarTripTraveler(HTMLCalendar):
    def __init__(self, year=None, month=None):
        super(CalendarTripTraveler, self).__init__()
        self.year = year
        self.month = month


    def formatday(self, day, events):
        events_per_day = events.filter(Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month=self.month, end_date__month=self.month,
                          start_date__day__lte=day, end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month__lt=self.month, end_date__month__gt=self.month)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month__lt=self.month, end_date__month=self.month,
                          end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year=self.year,
                          start_date__month=self.month, end_date__month__gt=self.month,
                          start_date__day__lte=day)|
                        Q(start_date__year__lt=self.year, end_date__year__gt=self.year)|
                        Q(start_date__year__lt=self.year, end_date__year=self.year,
                          end_date__month__gt=self.month)|
                        Q(start_date__year__lt=self.year, end_date__year=self.year,
                          end_date__month=self.month, end_date__day__gte=day)|
                        Q(start_date__year=self.year, end_date__year__gt=self.year,
                          start_date__month__lt=self.month)|
                        Q(start_date__year=self.year, end_date__year__gt=self.year,
                          start_date__month=self.month, start_date__day__lte=day))
        d = ''
        for event in events_per_day:
            d += f'<li>{event.get_detail_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True, **kwargs):

        events = Trip.objects.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                       start_date__month__lte=self.month, end_date__month__gte=self.month) |
                                     Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                     Q(start_date__year__lt=self.year, end_date__year=self.year,
                                        end_date__month__gte=self.month) |
                                     Q(start_date__year=self.year, end_date__year__gt=self.year,
                                        start_date__month__lte=self.month)).filter(user_id=kwargs['userid'])

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal+'</table>'


class CalendarAvailPriv(HTMLCalendar):
    def __init__(self, year=None, month=None, **kwargs):
        super(CalendarAvailPriv, self).__init__(**kwargs)
        self.year = year
        self.month = month

    def formatday(self, day, events):
        events_per_day = events.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month=self.month, end_date__month=self.month,
                                         start_date__day__lte=day, end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month__lt=self.month, end_date__month__gt=self.month) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month__lt=self.month, end_date__month=self.month,
                                         end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month=self.month, end_date__month__gt=self.month,
                                         start_date__day__lte=day) |
                                       Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                       Q(start_date__year__lt=self.year, end_date__year=self.year,
                                         end_date__month__gt=self.month) |
                                       Q(start_date__year__lt=self.year, end_date__year=self.year,
                                         end_date__month=self.month, end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year__gt=self.year,
                                         start_date__month__lt=self.month) |
                                       Q(start_date__year=self.year, end_date__year__gt=self.year,
                                         start_date__month=self.month, start_date__day__lte=day))
        d = ''
        for event in events_per_day:
            d += f'<li>{event.get_html_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True,**kwargs):
        # User = settings.settings.AUTH_USER_MODEL

        events = Available.objects.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                       start_date__month__lte=self.month, end_date__month__gte=self.month) |
                                     Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                     Q(start_date__year__lt=self.year, end_date__year=self.year,
                                       end_date__month__gte=self.month) |
                                     Q(start_date__year=self.year, end_date__year__gt=self.year,
                                       start_date__month__lte=self.month)).filter(user_id=kwargs['user_id'])
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal + '</table>'


class CalendarAvailHost(HTMLCalendar):
    def __init__(self, year=None, month=None, **kwargs):
        super(CalendarAvailHost, self).__init__(**kwargs)
        self.year = year
        self.month = month

    def formatday(self, day, events):
        events_per_day = events.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month=self.month, end_date__month=self.month,
                                         start_date__day__lte=day, end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month__lt=self.month, end_date__month__gt=self.month) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month__lt=self.month, end_date__month=self.month,
                                         end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year=self.year,
                                         start_date__month=self.month, end_date__month__gt=self.month,
                                         start_date__day__lte=day) |
                                       Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                       Q(start_date__year__lt=self.year, end_date__year=self.year,
                                         end_date__month__gt=self.month) |
                                       Q(start_date__year__lt=self.year, end_date__year=self.year,
                                         end_date__month=self.month, end_date__day__gte=day) |
                                       Q(start_date__year=self.year, end_date__year__gt=self.year,
                                         start_date__month__lt=self.month) |
                                       Q(start_date__year=self.year, end_date__year__gt=self.year,
                                         start_date__month=self.month, start_date__day__lte=day))
        d = ''
        for event in events_per_day:
            d += f'<li>{event.get_detail_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True,**kwargs):
        # User = settings.settings.AUTH_USER_MODEL

        events = Available.objects.filter(Q(start_date__year=self.year, end_date__year=self.year,
                                       start_date__month__lte=self.month, end_date__month__gte=self.month) |
                                     Q(start_date__year__lt=self.year, end_date__year__gt=self.year) |
                                     Q(start_date__year__lt=self.year, end_date__year=self.year,
                                       end_date__month__gte=self.month) |
                                     Q(start_date__year=self.year, end_date__year__gt=self.year,
                                       start_date__month__lte=self.month)).filter(user_id=kwargs['userid'])
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal + '</table>'
