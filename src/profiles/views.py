from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm

from django.contrib.auth.decorators import login_required   #for function based views use this decorator
# Create your views here.

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile) #instance = profile gives a particular user bio for instant edit
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, "profiles/main.html", context)