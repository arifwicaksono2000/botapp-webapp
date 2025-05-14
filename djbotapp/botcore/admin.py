from django.contrib import admin
from .models import Token, Subaccount, Milestone, History, HistoryDetail

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'expires_at')
    search_fields = ('user__username',)

@admin.register(Subaccount)
class SubaccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_id', 'platform', 'is_default')
    list_filter = ('platform', 'is_default')
    search_fields = ('user__username', 'account_id')

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'starting_balance', 'profit_goal', 'ending_balance')
    search_fields = ('starting_balance',)

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'subaccount', 'pair', 'opened_at', 'closed_at')
    list_filter = ('pair',)
    search_fields = ('user__username',)

@admin.register(HistoryDetail)
class HistoryDetailAdmin(admin.ModelAdmin):
    list_display = ('history', 'position_type', 'entry_price', 'exit_price', 'profit_loss', 'is_liquidated')
    list_filter = ('position_type', 'is_liquidated')
