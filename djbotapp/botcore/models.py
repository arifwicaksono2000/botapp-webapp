from django.db import models
from django.contrib.auth.models import User
import uuid

# User table were already defined in the library definition above
# User management (for web login)
# class User(AbstractUser):
#     pass

# API tokens for bot connection
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    access_token = models.TextField()
    refresh_token = models.TextField()
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token {self.pk}"

# Subaccounts management (IC Markets via cTrader platform)
class Subaccount(models.Model):
    PLATFORM_CHOICES = [
        ('ctrader', 'cTrader'),
        ('mt4', 'MetaTrader 4'),
        ('mt5', 'MetaTrader 5'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subaccounts')
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='ctrader')
    account_id = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=4)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.platform})"

# Milestone checkpoints for hedging strategy
class Milestone(models.Model):
    starting_balance = models.DecimalField(max_digits=15, decimal_places=4)
    loss = models.DecimalField(max_digits=15, decimal_places=4)
    profit_goal = models.DecimalField(max_digits=15, decimal_places=4)
    lot_size = models.DecimalField(max_digits=10, decimal_places=4)
    ending_balance = models.DecimalField(max_digits=15, decimal_places=4)

    def __str__(self):
        return f"Milestone Level {self.id}"
    
# History records for each hedging trade session
class Segments(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subaccount_id = models.ForeignKey(Subaccount, on_delete=models.SET_NULL, null=True, blank=True)
    milestone_id = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True, blank=True)
    total_positions = models.IntegerField
    total_balance = models.DecimalField(max_digits=15, decimal_places=4)
    pair = models.CharField(max_length=10, default='EURUSD')
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Hedging Session {self.id} ({self.pair})"
    
class Trades(models.Model):
    CURRENT_ACTIVE_TYPE = [
        ('L', 'Long'),
        ('S', 'Short'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    curr_active = models.CharField(max_length=10, choices=CURRENT_ACTIVE_TYPE)
    current_level = models.IntegerField
    achieved_level = models.IntegerField
    starting_balance = models.DecimalField(max_digits=15, decimal_places=4)
    profit_goal = models.DecimalField(max_digits=15, decimal_places=4)
    ending_balance = models.DecimalField(max_digits=15, decimal_places=4)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Trades Balance {self.starting_balance}"



# Individual trade details for hedging (always pairs of Long & Short)
class TradeDetail(models.Model):
    POSITION_TYPE_CHOICES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]

    # LIQUIDATION_CHOICES = [
    #     ('none', 'None yet'),
    #     ('long_liquidated', 'Long liquidated'),
    #     ('short_liquidated', 'Short liquidated'),
    #     ('both_loss', 'Both positions liquidated'),
    # ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    trade_id = models.ForeignKey(Trades, on_delete=models.CASCADE, related_name='details')
    position_type = models.CharField(max_length=10, choices=POSITION_TYPE_CHOICES)
    entry_price = models.DecimalField(max_digits=20, decimal_places=10)
    exit_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    pips = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    latest_balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_liquidated = models.BooleanField(default=False)
    # liquidation_status = models.CharField(max_length=20, choices=LIQUIDATION_CHOICES, default='none')
    lot_size = models.DecimalField(max_digits=10, decimal_places=2)
    response = models.TextField()
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.position_type.title()} | {self.entry_price} ({'Closed' if self.closed_at else 'Open'})"
