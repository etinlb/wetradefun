from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from user.forms import *
 
class LoginForm(forms.Form):
  """ 
  Form for creating new login
  """
  usern = forms.CharField()
  passw = forms.CharField(widget=forms.PasswordInput)

  def clean(self):
    try:

      
    except KeyError:
      # didn't find what we expected in data - fields are blank on front end.  Fields
      # are required by default so we don't need to worry about validation
      pass
    # return self.cleaned_data
