"""
URL configuration for djbotapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.shortcuts import redirect
from botcore import views

urlpatterns = [
    # Django Admin panel
    path('admin/', admin.site.urls),
    path('trades/', views.trades_view, name='trades'),

    # Your dashboard view (protected by @login_required)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('start_trade/', views.start_trade, name='start_trade'),

    path('emergency-close/', views.emergency_close, name='emergency_close'),

    path('accounts/', include('django.contrib.auth.urls')),

    # Root URL:
    # - If user is logged in → redirect to /dashboard/
    # - If not → redirect to /admin/login/
    path('', lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('/admin/login/')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )


