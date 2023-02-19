from django.contrib import admin

from .models import Account, Update

@admin.action(description='Mark selected slippi tags as approved')
def make_approved(modeladmin, request, queryset):
    queryset.update(approved=True)


@admin.action(description='Mark selected slippi tags as unapproved')
def make_unapproved(modeladmin, request, queryset):
    queryset.update(approved=False)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('slippi_tag', 'approved')
    actions = [make_approved, make_unapproved]


admin.site.register(Account,
    AccountAdmin,
)
admin.site.register(Update)