from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class CurrencyConversionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Convert currency",
        description="Convert an amount from one currency to another using live exchange rates.",
        parameters=[
            OpenApiParameter(
                name='amount',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Amount to convert'
            ),
            OpenApiParameter(
                name='from',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Source currency code (e.g., USD)'
            ),
            OpenApiParameter(
                name='to',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Target currency code (e.g., KES)'
            ),
        ],
        responses={
            200: {
                "example": {
                    "amount": 100,
                    "from": "USD",
                    "to": "KES",
                    "converted_amount": 13000,
                    "rate": 130
                }
            },
            400: {"description": "Bad request - missing or invalid parameters"},
            401: {"description": "Authentication required"},
            503: {"description": "Currency conversion service unavailable"}
        }
    )
    def get(self, request):
        # Get query parameters
        amount = request.query_params.get('amount')
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')

        # Validate parameters
        if not all([amount, from_currency, to_currency]):
            return Response({
                'error': 'Missing required parameters: amount, from, to'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({
                'error': 'Amount must be a valid number'
            }, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({
                'error': 'Amount must be positive'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate currency codes (basic check - 3 letters)
        if len(from_currency) != 3 or len(to_currency) != 3:
            return Response({
                'error': 'Currency codes must be 3 letters (e.g., USD, KES)'
            }, status=status.HTTP_400_BAD_REQUEST)

        # If same currency, return as-is
        if from_currency.upper() == to_currency.upper():
            return Response({
                'amount': amount,
                'from': from_currency.upper(),
                'to': to_currency.upper(),
                'converted_amount': amount,
                'rate': 1.0
            })

        try:
            # Use exchangerate.host API (free)
            api_url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return Response({
                        'amount': amount,
                        'from': from_currency.upper(),
                        'to': to_currency.upper(),
                        'converted_amount': data.get('result'),
                        'rate': data.get('info', {}).get('rate')
                    })
                else:
                    return Response({
                        'error': 'Invalid currency codes or conversion failed'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'Currency conversion service temporarily unavailable'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except requests.exceptions.Timeout:
            return Response({
                'error': 'Currency conversion service timeout'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except requests.exceptions.RequestException:
            return Response({
                'error': 'Currency conversion service unavailable'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
