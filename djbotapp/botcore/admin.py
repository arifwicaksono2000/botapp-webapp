from django.contrib import admin
from .models import (
    Token,
    Subaccount,
    Milestone,
    Segments,
    Trades,
    TradeDetail,
    Constant
)

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'is_used', 'expires_at', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'expires_at') # 'access_token' and 'refresh_token' might also be readonly depending on your use case

@admin.register(Subaccount)
class SubaccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'platform', 'account_id', 'balance', 'is_default')
    list_filter = ('platform', 'is_default')
    search_fields = ('user__username', 'account_id', 'name')

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
    search_fields = ('id', 'starting_balance',)

@admin.register(Segments)
class SegmentsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'subaccount_id',
        'total_positions',
        'total_balance',
        'pair',
        'opened_at',
        'closed_at',
        'status',
    )
    list_filter = ('pair', 'status', 'closed_at')
    search_fields = (
        'uuid',
        'subaccount__name', # Search by subaccount name
        'subaccount__account_id', # Search by subaccount ID
        'pair',
        'status'
    )

@admin.register(Trades)
class TradesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'segment_id',        # Uses the ForeignKey object, Django will display __str__
        'curr_active',
        'current_level',  # Uses the ForeignKey object, Django will display __str__
        'achieved_level', # Uses the ForeignKey object, Django will display __str__
        'starting_balance',
        'profit_goal',
        'ending_balance',
        'opened_at',
        'closed_at',
        'status', # Added status to list_display from your model
    )
    list_filter = ('curr_active', 'current_level', 'achieved_level', 'status')
    search_fields = (
        'uuid',
        'segment__uuid', # Search by segment UUID
        'current_level__id', # Search by milestone ID (if __str__ is not useful)
        'achieved_level__id', # Search by milestone ID
        'status'
    )

@admin.register(TradeDetail)
class TradeDetailAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'trade_id',          # Uses the ForeignKey object, Django will display __str__
        'segment_id',        # Uses the ForeignKey object, Django will display __str__
        'position_type',
        'entry_price',
        'exit_price',
        'pips',
        'lot_size',
        'is_liquidated',
        'opened_at',
        'closed_at',
    )
    list_filter = ('position_type', 'is_liquidated', 'opened_at', 'closed_at')
    search_fields = (
        'uuid',
        'trade__uuid', # Search by trade UUID
        'segment__uuid', # Search by segment UUID
        'position_type'
    )
    # Adding readonly_fields for created/closed timestamps
    readonly_fields = ('opened_at', 'closed_at')

@admin.register(Constant)
class ConstantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'variable',
        'value'
    )
    search_fields = ('variable',)