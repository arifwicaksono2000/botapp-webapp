from django.contrib import admin
from .models import (
    Token,
    Subaccount,
    Milestone,
    Segments,
    Trades,
    TradeDetail
)

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'is_used', 'expires_at', 'created_at')
    search_fields = ('user__username',)

@admin.register(Subaccount)
class SubaccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'platform', 'account_id', 'balance', 'is_default')
    list_filter = ('platform', 'is_default')
    search_fields = ('user__username', 'account_id')

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'starting_balance',
        'loss',
        'profit_goal',
        'lot_size',
        'ending_balance'
    )
    search_fields = ('starting_balance',)

@admin.register(Segments)
class SegmentsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'subaccount_id',
        'milestone_id',
        'total_positions',
        'total_balance',
        'pair',
        'opened_at',
        'closed_at',
    )
    list_filter = ('pair', 'closed_at')
    search_fields = ('uuid',)

@admin.register(Trades)
class TradesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'curr_active',
        'current_level',
        'achieved_level',
        'starting_balance',
        'profit_goal',
        'ending_balance',
        'opened_at',
        'closed_at',
    )
    list_filter = ('curr_active',)
    search_fields = ('uuid',)

@admin.register(TradeDetail)
class TradeDetailAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'trade_id',
        'position_type',
        'entry_price',
        'exit_price',
        'pips',
        'latest_balance',
        'lot_size',
        'is_liquidated',
        'opened_at',
        'closed_at',
    )
    list_filter = ('position_type', 'is_liquidated')
    search_fields = ('uuid', 'trade_id__id')
