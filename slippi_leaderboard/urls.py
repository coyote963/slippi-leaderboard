from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        '',
        include(
            ('leaderboard.urls',
            'leaderboard')

        )
    ),
    path('admin/', admin.site.urls),
]