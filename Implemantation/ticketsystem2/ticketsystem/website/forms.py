from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin import widgets


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class UserReg(forms.ModelForm):
    GENDER = (('M', 'Male'), ('F', 'Female'))

    gender = forms.ChoiceField(choices=GENDER, label='', initial='',
                               widget=forms.Select(), required=True)
    birthday = forms.CharField()
    phone_number = forms.CharField()

    class Meta:
        model = UserProfile
        fields = (
            'birthday',
            'gender',
            'phone_number',

        )


class BuyTicketForm(forms.Form):
    Quantity = (('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9))
    quantity = forms.ChoiceField(choices=Quantity, label='', initial='', required=True)


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name'
        )


