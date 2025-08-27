
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum
from categories.models import Category
from transactions.models import Transaction
from budgets.models import Budget
from .serializers import ReportSummarySerializer, ReportSummaryTotalsSerializer, FinancialHealthScoreSerializer
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class ReportSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get spending summary",
        description="Get spending summary grouped by category with budget comparison. Supports date filtering.",
        parameters=[
            OpenApiParameter(name='start_date', type=OpenApiTypes.DATE, description='Start date filter (YYYY-MM-DD)'),
            OpenApiParameter(name='end_date', type=OpenApiTypes.DATE, description='End date filter (YYYY-MM-DD)'),
            OpenApiParameter(name='month', type=OpenApiTypes.INT, description='Month filter (1-12)'),
            OpenApiParameter(name='year', type=OpenApiTypes.INT, description='Year filter (e.g., 2024)'),
        ]
    )
    def get(self, request):
        user = request.user
        # Filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        transactions = Transaction.objects.filter(user=user)
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        if month and year:
            transactions = transactions.filter(date__month=month, date__year=year)
        elif month:
            transactions = transactions.filter(date__month=month)
        elif year:
            transactions = transactions.filter(date__year=year)

        # Group by category
        category_sums = transactions.values('category__name').annotate(spent=Sum('amount'))

        # Get budgets for the period (if month/year provided, match period)
        # Optimize with select_related
        period = None
        if month and year:
            period = f"{year}-{str(month).zfill(2)}"
        budgets = Budget.objects.filter(user=user).select_related('category')
        if period:
            budgets = budgets.filter(period=period)
        budget_map = {b.category.name: b.amount for b in budgets}

        summary = []
        total_spent = 0
        total_budget = 0
        for cat in category_sums:
            cat_name = cat['category__name']
            spent = float(cat['spent'])
            budget = float(budget_map.get(cat_name, 0))
            remaining = budget - spent
            summary.append({
                'category': cat_name,
                'spent': spent,
                'budget': budget,
                'remaining': remaining
            })
            total_spent += spent
            total_budget += budget

        totals = {
            'spent': total_spent,
            'budget': total_budget,
            'remaining': total_budget - total_spent
        }

        return Response({
            'summary': summary,
            'totals': totals
        })


class FinancialHealthScoreView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get financial health score",
        description="Calculate a financial health score (0-100) based on budget adherence for the current month."
    )
    def get(self, request):
        user = request.user
        # Calculate total spent and total budget for the current month
        today = datetime.today()
        period = today.strftime('%Y-%m')
        transactions = Transaction.objects.filter(user=user, date__month=today.month, date__year=today.year)
        spent = transactions.aggregate(total=Sum('amount'))['total'] or 0
        budgets = Budget.objects.filter(user=user, period=period)
        budget_total = budgets.aggregate(total=Sum('amount'))['total'] or 0
        
        overspending = 0
        if budget_total > 0:
            overspending = max(0, (spent - budget_total) / budget_total)
        
        score = max(0, 100 - int(overspending * 100))
        
        if score >= 90:
            message = "Excellent! You're well within your budgets."
        elif score >= 75:
            message = "Good job! You're within most of your budgets."
        elif score >= 50:
            message = "Caution: You're approaching your budget limits."
        else:
            message = "Warning: You're overspending. Review your budgets."
        
        return Response({
            'score': score,
            'message': message
        })
