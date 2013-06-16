from profile.models import UserProfile, EducationProfile
from profile.forms import UserProfileForm, EducationProfileForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def show(request):
    profiles = UserProfile.objects.filter(owner=request.user)
    educationprofiles = EducationProfile.objects.filter(owner=request.user)
    context = {
        "profiles" : profiles,
        "educationprofiles" : educationprofiles
    }
    return render_to_response(
        'profile/show.html',
        context,
        context_instance = RequestContext(request)       
    )

def show_other(request, userhash):
    profiles = UserProfile.objects.filter(owner_hash=userhash)
    context = {
        "profiles" : profiles,
    }
    return render_to_response(
        'profile/show.html',
        context,
        context_instance = RequestContext(request)       
    )

def create(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, prefix='user_profile')
        education_profile_form = EducationProfileForm(request.POST, prefix='education_profile')
        
        if user_profile_form.is_valid() and education_profile_form.is_valid():
            user_profile = user_profile_form.save(commit = False)
            user_profile.owner = request.user
            user_profile.save()

            education_profile = education_profile_form.save(commit= False)
            education_profile.owner = request.user
            education_profile.save()
            #request.user.message_set.create(message='Profile has been created')

            if 'next' in request.POST:
                next = request.POST['next']
            else:
                next = reverse('profile_show')

            return HttpResponseRedirect(next)

    else:
        user_profile_form = UserProfileForm(prefix = 'user_profile')
        education_profile_form = EducationProfileForm(prefix='education_profile')    

    return render_to_response(
        'profile/create.html', 
        { 
            'user_profile_form' : user_profile_form,
            'education_profile_form' : education_profile_form 
        },
        context_instance = RequestContext(request),
    )
