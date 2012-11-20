# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from trades.forms import RegistrationForm
from trades.models import *



def sign_up(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            user = User.objects.create_user(
                form.cleaned_data['username'], 
                form.cleaned_data['email'], 
                form.cleaned_data['password'],)
            user_profile = UserProfile(user = user, account='account', address='address', rating=1)
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, 'Thanks for registering %s' % user.username)
            # Login the user
            login(request, user)
            # Send to home page

        else:
            if "__all__" in form._errors:
                messages.add_message(request, messages.ERROR, form._errors['__all__'])
    else:
        form = RegistrationForm() # An unbound form

    return render_to_response('users/sign.html', {
        'form': form,
    },
     context_instance=RequestContext(request))
#NOT FINISHED IN THE SLIGHTEST
def sign_in(request):
    form = RegistrationForm() # An unbound form
    return render_to_response('users/sign.html', {
        'form': form,
    },
     context_instance=RequestContext(request))

def account_management(request):
    return render_to_response('users/account_management.html')

# TODO handle loging in, session handling and account management buttons    


