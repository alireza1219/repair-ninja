"""
URL configuration for repair_ninja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    # Main Patterns
    path('', views.home_page_view),
    path('admin/', admin.site.urls),
    path('core/', include('repair_core.urls')),

    # Authentication patterns:
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('otp/', include('otp.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        # Debugging patterns:
        path('__debug__/', include('debug_toolbar.urls')),
        path('silk/', include('silk.urls', namespace='silk')),
    ]
