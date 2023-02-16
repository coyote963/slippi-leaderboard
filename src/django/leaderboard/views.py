from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import AccountForm

# POST/GET account
def account_request(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('leaderboard:index'))
    else:
        form = AccountForm()
    return render(
        request, 
        'leaderboard/account.html',
        {'form': form})

# GET /
def index(request):
    return render(request, 'leaderboard/home.html')
