from django import forms
from profile.models import UserProfile, EducationProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'date_of_birth', 'sex',)

class EducationProfileForm(forms.ModelForm):
    class Meta:
        model = EducationProfile
        exclude = ('owner',)
        fields = ('school_name', 'college_name')
