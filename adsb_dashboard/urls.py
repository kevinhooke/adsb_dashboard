"""
URL configuration for adsb_dashboard project.

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

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from dashboard import views

# replaced router approach
# router = routers.DefaultRouter()
# router.register('sbsmessage', views.SBSMessageViewSet)

urlpatterns = [
    # replaced, doesn't seem to work
    # path('api/', include(router.urls)),
    path("api/sbsmessage/", views.SBSMessageList.as_view()),
    path("api/sbsmessage/<int:pk>/", views.SBSMessageDetail.as_view()),
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
] + debug_toolbar_urls()

urlpatterns = format_suffix_patterns(urlpatterns)
