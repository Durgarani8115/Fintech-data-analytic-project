import csv
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta, date
from collections import defaultdict

from .models import Expense, Budget, SavingsGoal
from .serializers import ExpenseSerializer, BudgetSerializer, SavingsGoalSerializer
from .ml_model import generate_ai_predictions, predict_expense


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all().order_by('-date', '-created_at')
    serializer_class = ExpenseSerializer


class BudgetViewSet(ModelViewSet):
    queryset = Budget.objects.all().order_by('category')
    serializer_class = BudgetSerializer


class SavingsGoalViewSet(ModelViewSet):
    queryset = SavingsGoal.objects.all().order_by('-created_at')
    serializer_class = SavingsGoalSerializer


@api_view(['GET'])
def predict_view(request):
    """
    Returns AI-powered spending forecasts based on recorded expenses
    """
    expenses = Expense.objects.all()
    budgets = Budget.objects.all()
    prediction_data = generate_ai_predictions(expenses, budgets)
    return Response(prediction_data)


@api_view(['GET'])
def analytics_view(request):
    """
    Comprehensive financial analytics including totals, monthly breakdown, and budget comparisons
    """
    expenses = list(Expense.objects.all().order_by('date'))
    budgets = {b.category: b.monthly_limit for b in Budget.objects.all()}
    
    total_spent = sum(e.amount for e in expenses)
    expense_count = len(expenses)

    # Category breakdown
    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e.category] += float(e.amount)

    category_data = [
        {
            'category': cat,
            'amount': round(amt, 2),
            'budget': budgets.get(cat, 0.0),
            'percentage': round((amt / max(1.0, total_spent)) * 100, 1)
        }
        for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    ]

    # Monthly breakdown
    monthly_data_map = defaultdict(float)
    for e in expenses:
        m_key = e.date.strftime('%b %Y')
        monthly_data_map[m_key] += float(e.amount)

    monthly_data = [
        {'month': m, 'total': round(total, 2)}
        for m, total in monthly_data_map.items()
    ]

    # Current month metrics
    today = date.today()
    current_month_expenses = [
        e for e in expenses
        if e.date.year == today.year and e.date.month == today.month
    ]
    current_month_spent = sum(e.amount for e in current_month_expenses)
    total_monthly_budget = sum(budgets.values())

    return Response({
        'total_spent': round(total_spent, 2),
        'total_transactions': expense_count,
        'current_month_spent': round(current_month_spent, 2),
        'total_monthly_budget': round(total_monthly_budget, 2),
        'category_breakdown': category_data,
        'monthly_trends': monthly_data,
    })


@api_view(['GET'])
def export_csv_view(request):
    """
    Exports all expense records into a clean, downloadable CSV spreadsheet
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financial_expenses_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Category', 'Amount', 'Date', 'Payment Method', 'Description', 'Created At'])

    for exp in Expense.objects.all().order_by('-date'):
        writer.writerow([
            exp.id,
            exp.title,
            exp.category,
            exp.amount,
            exp.date.strftime('%Y-%m-%d'),
            exp.payment_method,
            exp.description,
            exp.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


@api_view(['POST', 'GET'])
def seed_demo_data_view(request):
    """
    Seeds rich demo data for presentation and immediate testing
    """
    default_budgets = [
        ('Housing & Rent', 12000.0),
        ('Food & Dining', 6000.0),
        ('Transportation', 3500.0),
        ('Utilities', 2500.0),
        ('Entertainment', 3000.0),
        ('Shopping', 4000.0),
        ('Healthcare', 2000.0),
    ]
    for cat, limit in default_budgets:
        Budget.objects.update_or_create(category=cat, defaults={'monthly_limit': limit})

    if not SavingsGoal.objects.exists():
        SavingsGoal.objects.create(
            title='Emergency Fund',
            target_amount=100000.0,
            current_amount=45000.0,
            target_date=date(2027, 6, 30),
            category='Security'
        )
        SavingsGoal.objects.create(
            title='Tech Gadgets / Laptop',
            target_amount=80000.0,
            current_amount=52000.0,
            target_date=date(2026, 12, 15),
            category='Electronics'
        )
        SavingsGoal.objects.create(
            title='Vacation Fund',
            target_amount=40000.0,
            current_amount=18000.0,
            target_date=date(2027, 3, 1),
            category='Travel'
        )

    if Expense.objects.count() < 5:
        today = date.today()
        sample_transactions = [
            ('Apartment Rent', 'Housing & Rent', 12000.0, today - timedelta(days=2), 'Net Banking', 'Monthly rent payment'),
            ('Grocery Supermarket', 'Food & Dining', 2450.0, today - timedelta(days=3), 'UPI', 'Weekly pantry restocking'),
            ('Electricity & Water Bill', 'Utilities', 1850.0, today - timedelta(days=5), 'Card', 'Power utility auto-debit'),
            ('Uber Commute to Campus', 'Transportation', 340.0, today - timedelta(days=6), 'UPI', 'Cab fare'),
            ('Netflix & Spotify Subs', 'Entertainment', 649.0, today - timedelta(days=8), 'Card', 'Streaming subscriptions'),
            ('Weekend Dining Out', 'Food & Dining', 1280.0, today - timedelta(days=9), 'Card', 'Dinner with college team'),
            ('Amazon Order - Books & Gear', 'Shopping', 2150.0, today - timedelta(days=12), 'Card', 'Reference books & accessories'),
            ('Fuel Refill', 'Transportation', 1500.0, today - timedelta(days=14), 'UPI', 'Petrol for vehicle'),
            ('Pharmacy & Vitamins', 'Healthcare', 820.0, today - timedelta(days=16), 'UPI', 'Prescriptions'),
            ('Cinema Tickets & Popcorn', 'Entertainment', 750.0, today - timedelta(days=18), 'Card', 'Weekend movie'),
            ('Coffee & Study Snacks', 'Food & Dining', 420.0, today - timedelta(days=20), 'UPI', 'Campus cafe'),
            
            ('Apartment Rent', 'Housing & Rent', 12000.0, today - timedelta(days=32), 'Net Banking', 'Rent payment'),
            ('Groceries & Supplies', 'Food & Dining', 3800.0, today - timedelta(days=35), 'Card', 'Monthly groceries'),
            ('Internet Broadband Bill', 'Utilities', 999.0, today - timedelta(days=38), 'UPI', 'Fiber internet'),
            ('Metro Smart Card Recharge', 'Transportation', 1000.0, today - timedelta(days=40), 'UPI', 'Metro commute card'),
            ('New Running Shoes', 'Shopping', 3200.0, today - timedelta(days=45), 'Card', 'Athletic sneakers'),
            ('Dentist Consultation', 'Healthcare', 1200.0, today - timedelta(days=48), 'Card', 'Routine dental checkup'),
            ('Dinner at Bistro', 'Food & Dining', 1650.0, today - timedelta(days=52), 'Card', 'Birthday celebration'),

            ('Apartment Rent', 'Housing & Rent', 12000.0, today - timedelta(days=62), 'Net Banking', 'Rent payment'),
            ('Grocery Market', 'Food & Dining', 3400.0, today - timedelta(days=66), 'UPI', 'Monthly groceries'),
            ('Electricity Utility', 'Utilities', 1600.0, today - timedelta(days=70), 'Card', 'Power bill'),
            ('Travel & Transit', 'Transportation', 2100.0, today - timedelta(days=75), 'UPI', 'Travel fare'),
            ('Gaming Subscription', 'Entertainment', 899.0, today - timedelta(days=80), 'Card', 'Online pass'),
        ]

        for title, category, amount, tx_date, payment, desc in sample_transactions:
            Expense.objects.create(
                title=title,
                category=category,
                amount=amount,
                date=tx_date,
                payment_method=payment,
                description=desc
            )

    return Response({
        'status': 'success',
        'message': 'Demo financial transactions, budgets, and savings goals seeded successfully.',
        'expense_count': Expense.objects.count(),
        'budget_count': Budget.objects.count(),
        'goal_count': SavingsGoal.objects.count()
    })
