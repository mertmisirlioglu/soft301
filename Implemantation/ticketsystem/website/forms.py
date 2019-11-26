from django import forms
from .models import User




    

class UserReg(forms.ModelForm):

    GENDER = (('M', 'Male'), ('F', 'Female'))
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender = forms.ChoiceField(choices=GENDER, label='', initial='',
                               widget=forms.Select(), required=True)
    email = forms.EmailField()
    birthday = forms.DateTimeField()
    phone_number = forms.CharField()
    password = forms.CharField()
    widgets = {'password': forms.PasswordInput()}

    class Meta:

        model = User
        fields = (
            'first_name',
            'last_name',
            'gender',
            'email',
            'birthday',
            'phone_number',
            'password',
            )

        
    
    