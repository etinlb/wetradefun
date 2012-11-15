from django import forms

class RegistrationForm(forms.Form):
  account = forms.CharField(max_length=64)
  password = forms.CharField(max_length=64)
  name = forms.CharField(max_length=64)
  email = forms.CharField(max_length=64)
  address = forms.CharField(max_length=64)