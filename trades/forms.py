from django import forms
from django.core import validators
from django.contrib.auth.models import User
from trades.models import *
 
class RegistrationForm(forms.Form):
  """ 
  Form for creating new login
  """
  username = forms.CharField()
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput)
  check_password = forms.CharField(widget=forms.PasswordInput)
  def clean(self):
    try:
      if self.cleaned_data['password'] != self.cleaned_data['check_password']:
        raise forms.ValidationError("Passwords entered do not match")
    except KeyError:
      # didn't find what we expected in data - fields are blank on front end.  Fields
      # are required by default so we don't need to worry about validation
      pass
    return self.cleaned_data

class MakeOfferForm(forms.Form):
  """ 
  Form for making offer
  """
  makeoffer_user_id = forms.IntegerField()
  makeoffer_game1_id = forms.IntegerField()
  makeoffer_game2_id = forms.IntegerField()
  def clean(self):
    try:
      if self.cleaned_data['makeoffer_game1_id']==self.cleaned_data['makeoffer_game2_id']:
        raise forms.ValidationError("These two games are the same")
      if len(Currentlist.objects.filter(gianBombID=self.cleaned_data['makeoffer_game2_id']))==0:
        raise forms.ValidationError("No one has target game")
    except KeyError:
      # didn't find what we expected in data - fields are blank on front end.  Fields
      # are required by default so we don't need to worry about validation
      pass
    return self.cleaned_data

class MakeOfferAjaxForm(forms.Form):
  """ 
  Form for making offer
  """
  makeofferajax_user_id = forms.IntegerField()
  makeofferajax_game1_id = forms.IntegerField()
  makeofferajax_game2_id = forms.IntegerField()

class EditOfferForm(forms.Form):
  editoffer_game1_id = forms.IntegerField()
