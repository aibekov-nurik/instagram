from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('inst_web/', include('inst_web.urls')),
    path('', lambda request: redirect('accounts/login/')),
]
