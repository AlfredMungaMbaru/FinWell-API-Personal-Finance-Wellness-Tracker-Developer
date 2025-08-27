
# Serializers for report endpoints (can be expanded for OpenAPI docs)
from rest_framework import serializers

class ReportSummarySerializer(serializers.Serializer):
	category = serializers.CharField()
	spent = serializers.FloatField()
	budget = serializers.FloatField()
	remaining = serializers.FloatField()

class ReportSummaryTotalsSerializer(serializers.Serializer):
	spent = serializers.FloatField()
	budget = serializers.FloatField()
	remaining = serializers.FloatField()

class FinancialHealthScoreSerializer(serializers.Serializer):
	score = serializers.IntegerField()
	message = serializers.CharField()
