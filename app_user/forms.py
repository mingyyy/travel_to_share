from django import forms
from .models import User, Language, ProfileTraveler, ProfileHost, Space, Program, Topic, Link
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

# from django.db import transaction
# from ktag.fields import TagField
from .constants import SUBJECT_LIST, LANGUAGE_LIST, SUBJECT_CHOICE
from django_google_maps.widgets import GoogleMapsAddressWidget

from django.forms import formset_factory


class FormRegister(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ['type', 'username', 'email', 'password1', 'password2']
        widgets = {'type': forms.RadioSelect,}

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     if self.type == '0' or self.type == '1':
    #         user.save()
    #     return user


class FormUserUpdate(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class FormProfileTravelerUpdate(forms.ModelForm):
    '''input_formats=['%Y/%m/%d']'''
    phone = PhoneNumberField(widget=forms.TextInput(attrs={}), label='Phone Number', required=False)
    birth_date = forms.DateField(input_formats=['%Y-%m-%d'], required=False)
    languages = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Language.objects.all(),
        help_text='Only those languages you master professionally.')

    class Meta:
        model = ProfileTraveler
        fields = ['gender', 'birth_date', 'nationality', 'phone', 'languages', 'photo']
        labels = {'nationality': 'Where are you from',
                  'photo': 'Profile picture',
                   }


class FormProfileTravelerUpdate2(forms.ModelForm):
    expertise = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Topic.objects.all(), label='Areas of expertise')

    class Meta:
        model = ProfileTraveler
        fields = ['bio', 'expertise', 'experience']
        labels = {'experience': 'More of your expertise', }
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder':
                  'Tell us more about yourself: what do you like, what is your dream, where have you been, etc.', }, ),
            'experience': forms.Textarea(attrs={
                'placeholder': 'Tell us more about your expertise and professional experience.'},),
                }


class FormProfileHostUpdate(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
                             label="Phone number", required=False)

    class Meta:
        model = ProfileHost
        fields = ['photo', 'name', 'type', 'phone', 'description', 'address', 'geolocation']
        labels = {'photo': "Profile picture",
                  'name': "Organization Name",
                  'type': "Organization Type",
                  }
        widgets = {"address": GoogleMapsAddressWidget,
            "geolocation": forms.Textarea(attrs={'placeholder': 'To be filled automatically.',}),
            'description': forms.Textarea(attrs={'placeholder': 'Tell us more about your organization.'})
                   }


class FormProfileHostUpdate2(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all(),
                help_text='Press Ctrl/Command to select multiple languages needed for the events.')
    interests = forms.ModelMultipleChoiceField(queryset=Topic.objects.all(), label='Subjects of interest',
                help_text='Press Ctrl/Command to select multiple subjects.')

    class Meta:
        model = ProfileHost
        fields = ['interests', 'interest_details', 'languages']
        labels = {
                  'interest_details': "More of your interest",
                  }
        widgets = {
            'interest_details': forms.Textarea(attrs={'placeholder': 'Please share with us the details of your need.'})
                   }



class FormSpace(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['title', 'detail', 'photo']
        label = {'title': "What you offer", "photo": "Picture of the Space"}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Meeting room for 50 people',}),
            'detail': forms.Textarea(attrs={'placeholder': 'Details of the space, equipments etc',}),
        }


class FormProgram(forms.ModelForm):

    class Meta:
        model = Program
        fields = ['subject', 'type', 'frequency', 'duration', 'title', 'description', 'requirement']
        labels = {'type': 'What kind of event?',
                  'frequency': 'Single or multiple events?',
                  'duration': 'How long is the event (per section)?',
                  }


class DeleteProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = []


class DeleteSpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = []

# testing dynamic form - link
class LinkForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'label': 'Link name',
            'class': 'form-control',
            'placeholder': 'e.g. facebook'
        })
    )

    url = forms.URLField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. www.facebook.com/your account/',
            'rows': 1,
            'cols': 20,
        })
    )

LinkFormset = formset_factory(LinkForm, extra=1)

class DeleteLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = []

# testing address
class FormAddress(forms.ModelForm):
    class Meta:
        model = ProfileHost
        fields = ['address', 'geolocation',]
        widgets = {
            "address": GoogleMapsAddressWidget,
            "geolocation": forms.TextInput(attrs={'placeholder': 'To be filled automatically.',
                                                 'rows': 1,
                                                 'cols': 10, })
        }


# testing language
# class FormLanguage(forms.ModelForm):
#     language = TagField(label='Language:', delimiters=',', data_list=LANGUAGE_LIST, initial='English')
#
#     class Meta:
#         model = ProfileTraveler
#         fields = ['language',]
#         widgets = {'language': forms.Textarea(attrs={'help_text': 'Only languages you master professionally.'})}
#         labels = {'language': 'Languages'}



