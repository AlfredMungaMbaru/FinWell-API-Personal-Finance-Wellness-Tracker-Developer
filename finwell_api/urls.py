from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def root_redirect(request):
    """Redirect root URL to API documentation"""
    return redirect('/api/docs/')

def api_root(request):
    """API root endpoint with basic information"""
    return HttpResponse("""
    <h1>FinWell API - Personal Finance Wellness Tracker</h1>
    <p>Welcome to the FinWell API!</p>
    <h2>Available Endpoints:</h2>
    <ul>
        <li><a href="/api/docs/">📚 Interactive API Documentation (Swagger UI)</a></li>
        <li><a href="/api/redoc/">📖 Alternative Documentation (ReDoc)</a></li>
        <li><a href="/api/schema/">🔧 OpenAPI Schema (JSON)</a></li>
        <li><a href="/admin/">🔧 Admin Panel</a></li>
    </ul>
    <h2>Quick Start:</h2>
    <ol>
        <li>Register a new user: <code>POST /api/register/</code></li>
        <li>Get JWT token: <code>POST /api/token/</code></li>
        <li>Use the token to access protected endpoints</li>
    </ol>
    <p><strong>For interactive testing, visit the <a href="/api/docs/">Swagger UI</a></strong></p>
    """, content_type='text/html')

urlpatterns = [
    path('', root_redirect, name='root'),
    path('api/', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/budgets/', include('budgets.urls')),
    path('api/reports/', include('reports.urls')),
    # Swagger/OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]