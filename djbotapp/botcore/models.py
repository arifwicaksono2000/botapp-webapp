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
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('successful', 'Successful'),
        ('liquidated', 'Liquidated'),
    ]

    uuid = models.CharField(max_length=36, default=uuid.uuid4, editable=False, unique=True)
    subaccount = models.ForeignKey(Subaccount, on_delete=models.SET_NULL, null=True, blank=True)
    total_positions = models.IntegerField()
    total_balance = models.DecimalField(max_digits=15, decimal_places=4)
    pair = models.CharField(max_length=10, default='EURUSD')
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,        # Maximum length for the status string
        choices=STATUS_CHOICES, # Use the defined choices
        default='running',    # Set a default status for new segments
        help_text="Current status of segments session"
    )
    is_pivot = models.BooleanField(default=False)

    def __str__(self):
        return f"Hedging Session {self.id} ({self.pair})"
    
class Trades(models.Model):
    CURRENT_ACTIVE_TYPE = [
        ('L', 'Long'),
        ('S', 'Short'),
        ('B', 'Both'),
        ('N', 'None'), # Both got liquidated
    ]

    STATUS_CHOICES = [
        ('running', 'Running'),
        ('successful', 'Successful'),
        ('liquidated', 'Liquidated'),
    ]

    uuid = models.CharField(max_length=36, default=uuid.uuid4, editable=False, unique=True)
    segment = models.ForeignKey(Segments, on_delete=models.SET_NULL, null=True, blank=True)
    curr_active = models.CharField(max_length=10, choices=CURRENT_ACTIVE_TYPE)
    
    # --- FIX IS HERE ---
    current_level = models.ForeignKey(
        Milestone, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='current_level_trades'  # Added related_name
    )
    achieved_level = models.ForeignKey(
        Milestone, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='achieved_level_trades' # Added related_name
    )
    # --- END OF FIX ---

    starting_balance = models.DecimalField(max_digits=15, decimal_places=4)
    profit_goal = models.DecimalField(max_digits=15, decimal_places=4)
    ending_balance = models.DecimalField(null=True, blank=True, max_digits=15, decimal_places=4)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='running',
        help_text="Current status of the hedging session"
    )

    def __str__(self):
        return f"Trades Balance {self.starting_balance}"


# Individual trade details for hedging (always pairs of Long & Short)
class TradeDetail(models.Model):
    POSITION_TYPE_CHOICES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]

    STATUS_CHOICES = [
        ('running', 'Running'),
        ('successful', 'Successful'),
        ('liquidated', 'Liquidated'),
        ('closed', 'CLOSED'),
    ]

    uuid = models.CharField(max_length=36, default=uuid.uuid4, editable=False, unique=True)
    trade = models.ForeignKey(Trades, on_delete=models.CASCADE, related_name='details')
    segment = models.ForeignKey(Segments, on_delete=models.SET_NULL, null=True, blank=True)
    position_id = models.BigIntegerField()
    position_type = models.CharField(max_length=10, choices=POSITION_TYPE_CHOICES)
    entry_price = models.DecimalField(max_digits=20, decimal_places=10)
    exit_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    pips = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='running',
        help_text="Current status each trade detail"
    )
    lot_size = models.DecimalField(max_digits=10, decimal_places=2)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.position_type.title()} | {self.entry_price} ({'Closed' if self.closed_at else 'Open'})"
    
# Milestone checkpoints for hedging strategy
class Constant(models.Model):
    variable = models.TextField()
    value = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Defined Variable {self.variable}"
