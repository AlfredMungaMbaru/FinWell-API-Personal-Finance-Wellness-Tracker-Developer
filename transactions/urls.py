from django.urls import path
from transactions.views import TransactionListCreateView, TransactionDetailView

urlpatterns = [
	path('', TransactionListCreateView.as_view(), name='transaction-list-create'),
	path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]
