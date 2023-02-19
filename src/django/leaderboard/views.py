from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max, F
from django.db import connection

from .forms import AccountForm
from .models import Update, Account

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


def generate_rankings_table():
    accounts = Account.objects.filter(current_update__isnull=False)
    updates = Update.objects.filter(account__in=accounts).order_by('-id')
    ranking_changes = updates.values('account').annotate(
        current_ranking=F('ranking'),
        last_ranking=F('account__previous_update__ranking')
    ).values('account', 'current_ranking', 'last_ranking')
    ranking_changes_dict = {
        change['account']: (change['current_ranking'], change['last_ranking']) 
        for change in ranking_changes
    }

    account_rows = []
    for account in accounts:
        current_rating = account.current_update.rating
        current_ranking = account.current_update.ranking
        ranking_change = ranking_changes_dict[account.id]
        if None in ranking_change:
            ranking_change = 0
        else:
            ranking_change = ranking_change[1] - ranking_change[0]
        account_rows.append(
            {
                'slippi_tag': account.slippi_tag,
                'display_name': account.display_name,
                'current_rating': current_rating,
                'current_ranking': current_ranking,
                'ranking_change': ranking_change
            }
        )
    return sorted(
        account_rows,
        key=lambda x: x['current_ranking'])
F

# GET /
# def index(request):
def index(request):
    account_rows = generate_rankings_table()
    return render(request, 'leaderboard/leaderboard.html', { 'account_rows': account_rows })
