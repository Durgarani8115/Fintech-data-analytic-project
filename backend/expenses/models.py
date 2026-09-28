from django.db import models
from django.utils import timezone

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food & Dining', 'Food & Dining'),
        ('Transportation', 'Transportation'),
        ('Housing & Rent', 'Housing & Rent'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Healthcare', 'Healthcare'),
        ('Shopping', 'Shopping'),
        ('Education', 'Education'),
        ('Personal Care', 'Personal Care'),
        ('Other', 'Other'),
    ]

    PAYMENT_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('UPI', 'UPI'),
        ('Net Banking', 'Net Banking'),
        ('Cash', 'Cash'),
    ]

    title = models.CharField(max_length=200, default='Expense')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Other')
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Card')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ${self.amount:.2f} ({self.category})"


class Budget(models.Model):
    category = models.CharField(max_length=100, unique=True)
    monthly_limit = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category}: ${self.monthly_limit:.2f}/month"


class SavingsGoal(models.Model):
    title = models.CharField(max_length=200)
    target_amount = models.FloatField()
    current_amount = models.FloatField(default=0.0)
    target_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}: ${self.current_amount} / ${self.target_amount}"
