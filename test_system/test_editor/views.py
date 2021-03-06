from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from user_pref.models import UserPreferences, Preference
from django.shortcuts import render
from test_system import base_path


@login_required
def redirect(request):
    qs = UserPreferences.objects.filter(user=request.user)
    if qs[0].user_preference == Preference.ADMIN or qs[0].user_preference == Preference.TEACHER:
        return render(request, 'test_editor.html', {})
    else:
        return HttpResponseRedirect(base_path.BASE_PATH + 'stream_choose/choose/')

@login_required
def redirect_add(request):
    qs = UserPreferences.objects.filter(user=request.user)
    if qs[0].user_preference == Preference.ADMIN or qs[0].user_preference == Preference.TEACHER:
        return render(request, 'add_question.html', {})
    else:
        return HttpResponseRedirect(base_path.BASE_PATH + 'stream_choose/choose/')
