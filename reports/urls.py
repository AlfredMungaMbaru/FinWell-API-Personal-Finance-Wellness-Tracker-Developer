
from django.urls import path
from . import views

urlpatterns = [
	path('summary/', views.ReportSummaryView.as_view(), name='report-summary'),
	path('health-score/', views.FinancialHealthScoreView.as_view(), name='report-health-score'),
]
