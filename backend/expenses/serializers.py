from rest_framework import serializers
from .models import Expense, Budget, SavingsGoal

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class SavingsGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = SavingsGoal
        fields = '__all__'

    def get_progress_percentage(self, obj):
        if obj.target_amount <= 0:
            return 0
        return round(min(100.0, (obj.current_amount / obj.target_amount) * 100), 1)
