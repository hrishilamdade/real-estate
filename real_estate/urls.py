from django.conf import settings

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/v1/auth/',include('djoser.urls')),
    path('api/v1/auth/',include('djoser.urls.jwt')),
    path('api/v1/profile/',include('apps.profiles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Real Estate Administration'
admin.site.site_title = 'Real Estate Admin Portal'
admin.site.index_title = 'Welcome to Real Estate Admin Portal'
