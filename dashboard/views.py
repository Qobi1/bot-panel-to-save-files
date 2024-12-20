from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bot.models import *

@login_required
def dashboard(request):
    users = TGUser.objects.all()
    files = Images.objects.all()
    return render(request, 'dashboard/dashboard.html', {'users': users, 'files': files})
