from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from expenses.views import (
    ExpenseViewSet,
    BudgetViewSet,
    SavingsGoalViewSet,
    predict_view,
    analytics_view,
    export_csv_view,
    seed_demo_data_view
)

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'goals', SavingsGoalViewSet, basename='goal')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/predict/', predict_view, name='predict'),
    path('api/analytics/', analytics_view, name='analytics'),
    path('api/export-csv/', export_csv_view, name='export_csv'),
    path('api/seed/', seed_demo_data_view, name='seed_demo_data'),
]
