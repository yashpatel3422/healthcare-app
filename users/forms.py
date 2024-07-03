from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, PatientProfile, DoctorProfile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    profile_picture = forms.ImageField(required=False)
    address_line1 = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)
    user_type = forms.ChoiceField(choices=(('patient', 'Patient'), ('doctor', 'Doctor')), required=True)


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=(('patient', 'Patient'), ('doctor', 'Doctor')))
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_patient = self.cleaned_data['user_type'] == 'patient'
        user.is_doctor = self.cleaned_data['user_type'] == 'doctor'
        
        if commit:
            user.save()
            if user.is_patient:
                PatientProfile.objects.create(user=user, 
                                              address_line1=self.cleaned_data['address_line1'],
                                              city=self.cleaned_data['city'],
                                              state=self.cleaned_data['state'],
                                              pincode=self.cleaned_data['pincode'],
                                              profile_picture=self.cleaned_data.get('profile_picture'))
            else:
                DoctorProfile.objects.create(user=user, 
                                             address_line1=self.cleaned_data['address_line1'],
                                             city=self.cleaned_data['city'],
                                             state=self.cleaned_data['state'],
                                             pincode=self.cleaned_data['pincode'],
                                             profile_picture=self.cleaned_data.get('profile_picture'))
        return user
