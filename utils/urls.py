from django.urls import path
from . import views

urlpatterns = [
    path('convert/', views.CurrencyConversionView.as_view(), name='currency-convert'),
]
