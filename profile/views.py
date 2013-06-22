from profile.models import UserProfile, EducationProfile
from profile.utils import ProfileUtils
from permissions.models import OwnerObjectPermissionsAssoc
from profile.forms import UserProfileForm, EducationProfileForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

# View function to show current users profile
def show(request):
    user_profile      = ProfileUtils.records_exist(
                            UserProfile.objects.filter(owner=request.user))
    education_profile = ProfileUtils.records_exist(
                            EducationProfile.objects.filter(owner=request.user))

    context = {
        "user_profile"      : user_profile,
        "education_profile" : education_profile
    }
    return render_to_response(
        'profile/show.html',
        context,
        context_instance = RequestContext(request)       
    )

# View function to show profile of others using generated hash
def show_other(request, userhash):
    
    user_profile      = ProfileUtils.records_exist(
                            UserProfile.objects.filter(owner_hash=userhash))
    if (user_profile == None):
        raise Http404

    education_profile = ProfileUtils.records_exist(
                            EducationProfile.objects.filter(
                                owner=user_profile.owner))
    
    if ((education_profile is not None) and 
        (OwnerObjectPermissionsAssoc.get_permissions(
                         user_profile.owner, request.user, 
                         'Education Profile', education_profile.id) != 'View')):
        education_profile = None
    
    context = {
        "user_profile"      : user_profile,
        "education_profile" : education_profile
    }
    return render_to_response(
        'profile/show.html',
        context,
        context_instance = RequestContext(request)       
    )

# View function to create various types of profiles based of profile_type
def create(request, profile_type):

    # No switch statement in python, need to use if/elif/else
    if profile_type == 'user_profile':
        class_name = 'UserProfileForm'
        submit_val = 'Create user profile'
    elif profile_type == 'education_profile':
        class_name = 'EducationProfileForm'
        submit_val = 'Create education profile'
    else:
        raise Http404

    if request.method == 'POST':
        form = eval(class_name + '(request.POST, prefix="' + profile_type + '")')

        if form.is_valid():
            profile = form.save(commit = False)
            profile.owner = request.user
            profile.save()

            if 'next' in request.POST:
                next = request.POST['next']
            else:
                next = reverse('profile_show')

            return HttpResponseRedirect(next)

    else:
        form = eval(class_name + '(prefix="' + profile_type + '")')
        form.submit_val = submit_val

    return render_to_response(
        'profile/create.html', 
        { 
            'form' : form,
        },
        context_instance = RequestContext(request),
    )
