"""
Daily job to update accounts
"""

from django.conf import settings
from django.core.cache import caches
from django_extensions.management.jobs import DailyJob

from leaderboard.management.commands.update_accounts import Command


class Job(DailyJob):
    help = "Update all the accounts"

    def execute(self):
        Command.run_update_accounts()