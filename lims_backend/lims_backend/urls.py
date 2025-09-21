"""
URL configuration for lims_backend project.

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
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path("admin/", admin.site.urls),

    # Default Running Succes
    path("", lambda request: JsonResponse({"message": "LIMS API Backend is running"})),

    # Authentication
    path("accounts/", include("accounts.urls")),

    # Samples
    path("samples/", include("samples.urls")),

    # Analysis
    path("analysis/", include("analysis.urls")),

    # Specs
    path("specs/", include("specs.urls")),

    # Complaints
    path("complaints/", include("complaints.urls")),

    # Documents
    path("documents/", include("documents.urls")),

    # Requests
    path("requests/", include("requests.urls")),

    # Inventory
    path("inventory/", include("inventory.urls")),

    # Report dan Audit trail
    path("reports/", include("reports.urls")),
]

