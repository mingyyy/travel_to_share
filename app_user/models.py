from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from .constants import CITIZENSHIP_CHOICE, GENDER_CHOICES, ORG_TYPE_CHOICE, SUBJECT_CHOICE, \
    EVENT_FREQ_CHOICE, EVENT_TYPE_CHOICE, EVENT_DURATION_CHOICE, EXPERTISE_CHOICE, LANGUAGE_CHOICE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_google_maps.fields import AddressField, GeoLocationField
from django.urls import reverse


class User(AbstractUser):
    TYPE_CHOICES = (('0', 'Traveler'), ('1', 'Local Host'))
    type = models.CharField(max_length=1, default=None, null=True, choices=TYPE_CHOICES, verbose_name='Account Type')

    REQUIRED_FIELDS = ['type', 'email']


class Language(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language

    class Meta:
        ordering = ('language',)


class Topic(models.Model):
    topic = models.CharField(max_length=50)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ('topic',)


class ProfileTravelerManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (models.Q(languages__language__icontains=query) |
                         models.Q(expertise__topic__icontains=query) |
                         models.Q(bio__icontains=query) |
                         models.Q(experience__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs


class ProfileTraveler(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    nationality = models.CharField(choices=CITIZENSHIP_CHOICE, max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_traveler')
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    languages = models.ManyToManyField(Language)
    expertise = models.ManyToManyField(Topic)
    experience = models.TextField(null=True, blank=True)

    objects = ProfileTravelerManager()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        '''resize fotos'''
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.photo.name)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.name)
        except FileNotFoundError as e:
                pass

    def get_absolute_url(self):
        return reverse('profile_traveler', kwargs={'userid': self.user.id})


class ProfileHostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (models.Q(languages__language__icontains=query) |
                         models.Q(interests__topic__icontains=query) |
                         models.Q(description__icontains=query) |
                         models.Q(interest_details__icontains=query) |
                         models.Q(address__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs


class ProfileHost(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False)
    type = models.CharField(choices=ORG_TYPE_CHOICE, max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    address = AddressField(max_length=200)
    geolocation = GeoLocationField(blank=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_host')
    interests = models.ManyToManyField(Topic)
    interest_details = models.TextField(blank=True)
    languages = models.ManyToManyField(Language)

    objects = ProfileHostManager()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        '''resize fotos'''
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.photo.name)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.name)
        except FileNotFoundError as e:
                pass

    def get_absolute_url(self):
        return reverse('profile_host', kwargs={'userid': self.user.id})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == '0':
            ProfileTraveler.objects.create(user=instance)
        elif instance.type == '1':
            ProfileHost.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if instance.type == '0':
        instance.profiletraveler.save()
    elif instance.type == '1':
        instance.profilehost.save()


class Program(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    subject = models.CharField(choices=SUBJECT_CHOICE, max_length=50)

    type = models.CharField(choices=EVENT_TYPE_CHOICE, max_length=30)
    frequency = models.CharField(choices=EVENT_FREQ_CHOICE, max_length=30)
    duration = models.CharField(choices=EVENT_DURATION_CHOICE, max_length=20)

    title = models.CharField(max_length=120, null=False)
    description = models.TextField()
    requirement = models.TextField()

    def __str__(self):
        return self.title


class Space(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    title = models.CharField(max_length=120, null=False)
    detail = models.TextField()
    photo = models.ImageField(default='default.jpg', upload_to='space_host')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        '''resize fotos'''
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.photo.name)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.name)
        except FileNotFoundError as e:
                pass


class Link(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False) # instagram
    url = models.URLField(null=False, blank=False) # www.instagram.com/xxxx/

    def __str__(self):
        return f'{self.name} - {self.url}'

    class Meta:
        ordering = ('name',)


class Publish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=False, blank=False)
    on_profile = models.BooleanField()
    on_program = models.BooleanField()
    on_space = models.BooleanField()
    on_trip = models.BooleanField()

    def __str__(self):
        return self.name
