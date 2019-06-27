from .models import Trip, Available
from django import forms
from app_user.constants import CITIZENSHIP_CHOICE_SHORT, DESTINATION_CHOICE_SHORT


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=50,required=True, help_text='50 characters max.')
    content = forms.CharField(widget= forms.Textarea(attrs={'placeholder': 'Enter your message here.'}),
                        required=True)

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ["user",]
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_date': forms.DateInput(),
            'end_date': forms.DateInput(),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ('%Y-%m-%d',)
        self.fields['end_date'].input_formats = ('%Y-%m-%d',)


class TripDeleteForm(forms.Form):
    confirm = forms.CharField(max_length=7, widget=forms.Textarea(attrs={'placeholder': 'confirm', 'rows': 1, 'cols': 4}),
                        required=False, label='')


class AvailableForm(forms.ModelForm):
    class Meta:
        model = Available
        exclude = ["user", ]
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_date': forms.DateInput(),
            'end_date': forms.DateInput(),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AvailableForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ('%Y-%m-%d',)
        self.fields['end_date'].input_formats = ('%Y-%m-%d',)


class AvailableDeleteForm(forms.Form):
    confirm = forms.CharField(max_length=7,
                              widget=forms.Textarea(attrs={'placeholder': 'confirm', 'rows': 1, 'cols': 4}),
                              required=False, label='')


class EntryRequirementForm(forms.Form):
    citizenship = forms.ChoiceField(label='Passport issued by which country?',
                              choices=CITIZENSHIP_CHOICE_SHORT, initial="US")

    destination = forms.ChoiceField(label='Which country are you visiting as a tourist?',
                              choices=DESTINATION_CHOICE_SHORT, initial="VN")
