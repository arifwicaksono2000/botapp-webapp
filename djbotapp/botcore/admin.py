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
    list_display = ('user', 'access_token', 'refresh_token', 'is_used', 'expires_at', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('access_token', 'refresh_token', 'expires_at', 'created_at')

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
        'subaccount',  # Changed from subaccount_id to show __str__
        'total_positions',
        'total_balance',
        'pair',
        'opened_at',
        'closed_at',
        'status',
        'is_pivot',  # Added new field
    )
    list_filter = ('pair', 'status', 'is_pivot', 'closed_at')
    search_fields = (
        'uuid',
        'subaccount__name',
        'subaccount__account_id',
        'pair',
        'status'
    )
    readonly_fields = ('opened_at', 'closed_at')


@admin.register(Trades)
class TradesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'segment',        # Changed from segment_id to show __str__
        'curr_active',
        'current_level',
        'achieved_level',
        'starting_balance',
        'profit_goal',
        'ending_balance',
        'opened_at',
        'closed_at',
        'status',
    )
    list_filter = ('curr_active', 'current_level', 'achieved_level', 'status')
    search_fields = (
        'uuid',
        'segment__uuid',
        'current_level__id',
        'achieved_level__id',
        'status'
    )
    readonly_fields = ('opened_at', 'closed_at')

@admin.register(TradeDetail)
class TradeDetailAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'trade',          # Changed from trade_id to show __str__
        'segment',        # Changed from segment_id to show __str__
        'position_id',    # Added new field
        'position_type',
        'entry_price',
        'exit_price',
        'pips',
        'lot_size',
        'status',
        'opened_at',
        'closed_at',
    )
    list_filter = ('position_type', 'status', 'opened_at', 'closed_at')
    search_fields = (
        'uuid',
        'trade__uuid',
        'segment__uuid',
        'position_id',
        'position_type'
    )
    readonly_fields = ('opened_at', 'closed_at')

@admin.register(Constant)
class ConstantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'variable',
        'value',
        'is_active'  # Added new field
    )
    list_filter = ('is_active',) # Added filter for is_active
    search_fields = ('variable',)